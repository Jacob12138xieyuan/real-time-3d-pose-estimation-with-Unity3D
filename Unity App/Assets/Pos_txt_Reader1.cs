using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System;
using System.Text;
using System.Linq;
using System.Net;
using System.Net.Sockets;
// pos.txtのデータ
// https://github.com/miu200521358/3d-pose-baseline-vmd/blob/master/doc/Output.md
// 0 :Hip
// 1 :RHip
// 2 :RKnee
// 3 :RFoot
// 4 :LHip
// 5 :LKnee
// 6 :LFoot
// 7 :Spine
// 8 :Thorax
// 9 :Neck/Nose
// 10:Head
// 11:LShoulder
// 12:LElbow
// 13:LWrist
// 14:RShoulder
// 15:RElbow
// 16:RWrist

public class Pos_txt_Reader1 : MonoBehaviour
{
    float scale_ratio = 0.001f;  // pos.txtとUnityモデルのスケール比率
                                 // pos.txtの単位はmmでUnityはmのため、0.001に近い値を指定。モデルの大きさによって調整する
    float heal_position = 0.00f; // 足の沈みの補正値(単位：m)。プラス値で体全体が上へ移動する
    float head_angle = 25f; // 顔の向きの調整 顔を15度上げる

    public string[] str = new string[52];
    //public String pos_filename; // pos.txtのファイル名
    public Boolean debug_cube; // デバッグ用Cubeの表示フラグ
    //public int start_frame; // 開始フレーム
    //public String end_frame; // 終了フレーム  
    //float play_time; // 再生時間 
    Transform[] bone_t; // モデルのボーンのTransform
    Transform[] cube_t; // デバック表示用のCubeのTransform
    Vector3 init_position; // 初期のセンターの位置
    Quaternion[] init_rot; // 初期の回転値
    Quaternion[] init_inv; // 初期のボーンの方向から計算されるクオータニオンのInverse
    //List<Vector3[]> pos; // pos.txtのデータを保持するコンテナ
    int[] bones = new int[10] { 1, 2, 4, 5, 7, 8, 11, 12, 14, 15 }; // 親ボーン
    int[] child_bones = new int[10] { 2, 3, 5, 6, 8, 10, 12, 13, 15, 16 }; // bonesに対応する子ボーン
    static int bone_num = 17;
    Animator anim;
    string data = null;
    int count = 1;
    int _port = 5005;
    int bytesRec = 0;
    byte[] buffer = new Byte[1024];
    IPEndPoint localEndPoint = null;
    Socket listener = null;
    Socket socket = null;
    static Vector3[] now_pos = new Vector3[bone_num];
    //int s_frame;
    //int e_frame;

    // pos.txtのデータを読み込み、リストで返す
    //List<Vector3[]> ReadPosData(string filename)
    //{
    //    List<Vector3[]> data = new List<Vector3[]>();

    //    List<string> lines = new List<string>();
    //    StreamReader sr = new StreamReader(filename);
    //    while (!sr.EndOfStream)
    //    {
    //        lines.Add(sr.ReadLine());
    //    }
    //    sr.Close();

    //    foreach (string line in lines)
    //    {
    //        //string line2 = line.Replace(",", "");
    //        string[] str = line.Split(new string[] { " " }, System.StringSplitOptions.RemoveEmptyEntries); // スペースで分割し、空の文字列は削除


    //        data.Add(vs);
    //    }
    //    return data;
    //}

    // BoneTransformの取得。回転の初期値を取得
    void GetInitInfo()
    {
        bone_t = new Transform[bone_num];
        init_rot = new Quaternion[bone_num];
        init_inv = new Quaternion[bone_num];

        bone_t[0] = anim.GetBoneTransform(HumanBodyBones.Hips);
        bone_t[1] = anim.GetBoneTransform(HumanBodyBones.RightUpperLeg);
        bone_t[2] = anim.GetBoneTransform(HumanBodyBones.RightLowerLeg);
        bone_t[3] = anim.GetBoneTransform(HumanBodyBones.RightFoot);
        bone_t[4] = anim.GetBoneTransform(HumanBodyBones.LeftUpperLeg);
        bone_t[5] = anim.GetBoneTransform(HumanBodyBones.LeftLowerLeg);
        bone_t[6] = anim.GetBoneTransform(HumanBodyBones.LeftFoot);
        bone_t[7] = anim.GetBoneTransform(HumanBodyBones.Spine);
        bone_t[8] = anim.GetBoneTransform(HumanBodyBones.Neck);
        bone_t[10] = anim.GetBoneTransform(HumanBodyBones.Head);
        bone_t[11] = anim.GetBoneTransform(HumanBodyBones.LeftUpperArm);
        bone_t[12] = anim.GetBoneTransform(HumanBodyBones.LeftLowerArm);
        bone_t[13] = anim.GetBoneTransform(HumanBodyBones.LeftHand);
        bone_t[14] = anim.GetBoneTransform(HumanBodyBones.RightUpperArm);
        bone_t[15] = anim.GetBoneTransform(HumanBodyBones.RightLowerArm);
        bone_t[16] = anim.GetBoneTransform(HumanBodyBones.RightHand);

        // Spine,LHip,RHipで三角形を作ってそれを前方向とする。
        Vector3 init_forward = TriangleNormal(bone_t[7].position, bone_t[4].position, bone_t[1].position);
        init_inv[0] = Quaternion.Inverse(Quaternion.LookRotation(init_forward));

        init_position = bone_t[0].position;
        init_rot[0] = bone_t[0].rotation;
        for (int i = 0; i < bones.Length; i++)
        {
            int b = bones[i];
            int cb = child_bones[i];

            // 対象モデルの回転の初期値
            init_rot[b] = bone_t[b].rotation;
            // 初期のボーンの方向から計算されるクオータニオン
            init_inv[b] = Quaternion.Inverse(Quaternion.LookRotation(bone_t[b].position - bone_t[cb].position, init_forward));
        }
    }

    // 指定の3点でできる三角形に直交する長さ1のベクトルを返す
    Vector3 TriangleNormal(Vector3 a, Vector3 b, Vector3 c)
    {
        Vector3 d1 = a - b;
        Vector3 d2 = a - c;

        Vector3 dd = Vector3.Cross(d1, d2);
        dd.Normalize();

        return dd;
    }

    // デバック用cubeを生成する。生成済みの場合は位置を更新する
    void UpdateCube()
    {
        if (cube_t == null)
        {
            // 初期化して、cubeを生成する
            cube_t = new Transform[bone_num];

            for (int i = 0; i < bone_num; i++)
            {
                Transform t = GameObject.CreatePrimitive(PrimitiveType.Cube).transform;
                t.transform.parent = this.transform;
                t.localPosition = now_pos[i] * scale_ratio;
                t.name = i.ToString();
                t.localScale = new Vector3(0.05f, 0.05f, 0.05f);
                cube_t[i] = t;

                Destroy(t.GetComponent<BoxCollider>());
            }
        }
        else
        {
            // モデルと重ならないように少しずらして表示
            Vector3 offset = new Vector3(1.2f, 0, 0);

            // 初期化済みの場合は、cubeの位置を更新する
            for (int i = 0; i < bone_num; i++)
            {
                cube_t[i].localPosition = now_pos[i] * scale_ratio + new Vector3(0, heal_position, 0) + offset;
            }
        }
    }

    void Start()
    {
        anim = GetComponent<Animator>();
        //play_time = 0;
        //if (System.IO.File.Exists(pos_filename) == false)
        //{
        //    Debug.Log("<color=blue>Error! Pos file not found(" + pos_filename + "). Check Pos_filename in Inspector.</color>");
        //}
        //pos = ReadPosData(pos_filename);
        GetInitInfo();


        localEndPoint = new IPEndPoint(IPAddress.Parse("192.168.1.212"), _port);
        listener = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        listener.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        listener.Bind(localEndPoint);
        
        
        
        //if (pos != null)
        //{
        //    // inspectorで指定した開始フレーム、終了フレーム番号をセット
        //    if (start_frame >= 0 && start_frame < pos.Count)
        //    {
        //        s_frame = start_frame;
        //    }
        //    else
        //    {
        //        s_frame = 0;
        //    }
        //    int ef;
        //    if (int.TryParse(end_frame, out ef))
        //    {
        //        if (ef >= s_frame && ef < pos.Count)
        //        {
        //            e_frame = ef;
        //        }
        //        else
        //        {
        //            e_frame = pos.Count - 1;
        //        }
        //    }
        //    else
        //    {
        //        e_frame = pos.Count - 1;
        //    }
        //    Debug.Log("End Frame:" + e_frame.ToString());
        //}
    }

    void Update()
    {
        
        listener.Listen(10);
        Debug.Log(count);
        socket = listener.Accept();

        int bytesRec = socket.Receive(buffer);
        data = Encoding.ASCII.GetString(buffer, 0, bytesRec);
        

        if (data != "" && data!=null)
        {
            count++;
            //Debug.Log(data);

            //byte[] msg = Encoding.ASCII.GetBytes(data);
            //socket.Send(msg);
            //socket.Shutdown(SocketShutdown.Both);
            //socket.Close();

            //socket = null;


            str = data.Split(' ');
            now_pos = new Vector3[bone_num];
            for (int i = 0; i < str.Length; i += 3)
            {
                now_pos[i / 3] = new Vector3(-float.Parse(str[i]), float.Parse(str[i + 2]), -float.Parse(str[i + 1]));
            }

            //play_time += Time.deltaTime;

            //int frame = s_frame + (int)(play_time * 30.0f);  // pos.txtは30fpsを想定
            //if (frame > e_frame)
            //{
            //    play_time = 0;  // 繰り返す
            //    frame = s_frame;
            //}

            if (debug_cube)
            {
                UpdateCube(); // デバッグ用Cubeを表示する
            }

            //Vector3[] now_pos = vs;

            // センターの移動と回転
            Vector3 pos_forward = TriangleNormal(now_pos[7], now_pos[4], now_pos[1]);
            bone_t[0].position = now_pos[0] * scale_ratio + new Vector3(init_position.x, heal_position, init_position.z);
            bone_t[0].rotation = Quaternion.LookRotation(pos_forward) * init_rot[0];

            // 各ボーンの回転
            for (int i = 0; i < bones.Length; i++)
            {
                int b = bones[i];
                int cb = child_bones[i];
                bone_t[b].rotation = Quaternion.LookRotation(now_pos[b] - now_pos[cb], pos_forward) * init_inv[b] * init_rot[b];
            }

            // 顔の向きを上げる調整。両肩を結ぶ線を軸として回転
            bone_t[8].rotation = Quaternion.AngleAxis(head_angle, bone_t[11].position - bone_t[14].position) * bone_t[8].rotation;

            buffer = new Byte[1024];
            data = null;
            bytesRec = 0;
        }
    }
}
