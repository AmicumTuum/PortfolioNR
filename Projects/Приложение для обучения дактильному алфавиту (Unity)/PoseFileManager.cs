using System.IO;
using UnityEngine;
using System.Collections;

public class PoseFileManager : MonoBehaviour
{
    private static bool posesResetThisSession = false;

    private string fileName = "default_poses.json";
    private string tempFileName = "default_poses_temp.json";

    private void Start()
    {
        if (!posesResetThisSession)
        {
            StartCoroutine(CopyPoseFileIfNeeded());
        }
        else
        {
            Debug.Log("���� ������ ��� ����������� ��� �������. ����������.");
        }
    }

    private IEnumerator CopyPoseFileIfNeeded()
    {
        string sourcePath = Path.Combine(Application.streamingAssetsPath, fileName);
        string destPath = Path.Combine(Application.temporaryCachePath, tempFileName);

        if (File.Exists(destPath))
        {
            File.Delete(destPath);
            Debug.Log("����� ���������� ��������� ���� ������.");
        }

#if UNITY_ANDROID && !UNITY_EDITOR
        using (var request = UnityEngine.Networking.UnityWebRequest.Get(sourcePath))
        {
            yield return request.SendWebRequest();

            if (request.result == UnityEngine.Networking.UnityWebRequest.Result.Success)
            {
                File.WriteAllBytes(destPath, request.downloadHandler.data);
                Debug.Log("���� ������ ���������� � ���.");
            }
            else
            {
                Debug.LogError("�� ������� ����������� �����: " + request.error);
            }
        }
#else
        if (File.Exists(sourcePath))
        {
            File.Copy(sourcePath, destPath, true);
            Debug.Log("���� ������ ���������� (Editor/PC).");
        }
        else
        {
            Debug.LogError("���� � StreamingAssets �� ������!");
        }
        yield return null;
#endif

        posesResetThisSession = true;
    }
}
