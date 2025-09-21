using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;
using TMPro;

public class UIButtonHoverEffect : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler, IPointerClickHandler
{
    public Image background;
    public TextMeshProUGUI label;

    public Color normalColor = new Color32(21, 145, 234, 255);   // обычная
    public Color hoverColor = new Color32(15, 175, 251, 255);    // при наведении
    public Color normalTextColor = new Color32(229, 252, 255, 255); // текст
    public Color hoverTextColor = Color.white;

    public float scaleAmount = 1.2f;
    public float transitionSpeed = 5f;
    public float clickScale = 0.9f;     // масштаб при клике
    public float clickDuration = 0.1f;  // как долго длится эффект

    private Vector3 originalScale;
    private Vector3 targetScale;
    private bool hovering = false;
    private float clickTimer = 0f;
    private bool clicked = false;

    void Start()
    {
        originalScale = transform.localScale;
        targetScale = originalScale;
        background.color = normalColor;
        label.color = normalTextColor;
    }

    void Update()
    {
        // Плавная анимация цвета и масштаба
        Color targetBG = hovering ? hoverColor : normalColor;
        Color targetText = hovering ? hoverTextColor : normalTextColor;

        background.color = Color.Lerp(background.color, targetBG, Time.deltaTime * transitionSpeed);
        label.color = Color.Lerp(label.color, targetText, Time.deltaTime * transitionSpeed);

        // Анимация нажатия
        if (clicked)
        {
            clickTimer += Time.deltaTime;
            if (clickTimer >= clickDuration)
            {
                clicked = false;
                clickTimer = 0f;
            }
        }

        // Установка целевого масштаба
        if (clicked)
            targetScale = originalScale * clickScale;
        else if (hovering)
            targetScale = originalScale * scaleAmount;
        else
            targetScale = originalScale;

        transform.localScale = Vector3.Lerp(transform.localScale, targetScale, Time.deltaTime * transitionSpeed * 2f);
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        hovering = true;
    }

    public void OnPointerExit(PointerEventData eventData)
    {
        hovering = false;
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        clicked = true;
        clickTimer = 0f;
    }
}