using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class GestureHintToggle : MonoBehaviour
{
    public GameObject hintImage;                // объект со спрайтом
    public TextMeshProUGUI buttonText;          // текст кнопки

    private bool isVisible = false;

    public void ToggleHint()
    {
        isVisible = !isVisible;
        hintImage.SetActive(isVisible);
        buttonText.text = isVisible ? "…" : "?";
    }
}