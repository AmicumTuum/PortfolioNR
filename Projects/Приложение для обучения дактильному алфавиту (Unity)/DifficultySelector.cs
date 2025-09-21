using UnityEngine;
using UnityEngine.SceneManagement;

public class DifficultySelector : MonoBehaviour
{
    public void SelectEasy() => LoadLevel("˸����");
    public void SelectMedium() => LoadLevel("�������");
    public void SelectHard() => LoadLevel("������");

    private void LoadLevel(string difficulty)
    {
        PlayerPrefs.SetString("Difficulty", difficulty);
        PlayerPrefs.Save();
        SceneManager.LoadScene("Level");
    }
}