using UnityEngine;
using UnityEngine.SceneManagement;

public class DifficultySelector : MonoBehaviour
{
    public void SelectEasy() => LoadLevel("Лёгкий");
    public void SelectMedium() => LoadLevel("Средний");
    public void SelectHard() => LoadLevel("Тяжёлый");

    private void LoadLevel(string difficulty)
    {
        PlayerPrefs.SetString("Difficulty", difficulty);
        PlayerPrefs.Save();
        SceneManager.LoadScene("Level");
    }
}