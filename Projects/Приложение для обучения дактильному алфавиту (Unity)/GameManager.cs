using System.Collections.Generic;
using UnityEngine;
using TMPro;
using System.IO;
using Oculus.Interaction.Input;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    [Header("UI")]
    public TMP_Text difficultyText;
    public TMP_Text wordText;
    public TMP_Text inputText;
    public TMP_Text timerText;
    [Header("End Game Stats")]
    [SerializeField] private TMP_Text skippedLettersText;
    [SerializeField] private TMP_Text skippedWordsText;

    [SerializeField] private GameObject endPanel;
    [SerializeField] private GameObject levelPanel;
    [SerializeField] private TMP_Text finalTimeText;
    private int skippedLetters = 0;
    private int skippedWords = 0;

    [Header("Hand")]
    public Hand userHand;

    [Header("Распознавание")]
    public float posThreshold = 0.04f;
    public float rotThreshold = 25f;

    private bool timerRunning = true;

    private Dictionary<string, Dictionary<HandJointId, Pose>> loadedPoses = new();
    private readonly HandJointId[] trackedJoints = new HandJointId[]
    {
        HandJointId.HandThumb1, HandJointId.HandThumb2, HandJointId.HandThumb3,
        HandJointId.HandIndex0, HandJointId.HandIndex1, HandJointId.HandIndex2, HandJointId.HandIndex3,
        HandJointId.HandMiddle0, HandJointId.HandMiddle1, HandJointId.HandMiddle2, HandJointId.HandMiddle3,
        HandJointId.HandRing0, HandJointId.HandRing1, HandJointId.HandRing2, HandJointId.HandRing3,
        HandJointId.HandPinky0, HandJointId.HandPinky1, HandJointId.HandPinky2, HandJointId.HandPinky3,
        HandJointId.HandWristRoot, HandJointId.HandPalm
    };

    private List<string> currentWords = new();
    private string currentWord = "";
    private string currentInput = "";
    private int currentLetterIndex = 0;
    private int currentWordIndex = 0;

    private float timer = 0f;
    private float gestureTimer = 0f;
    private float gestureCheckCooldown = 0.5f;



    void Start()
    {
        currentWords.Clear();
        currentWordIndex = 0;
        currentLetterIndex = 0;
        timer = 0f;
        skippedLetters = 0;
        skippedWords = 0;

        LoadPosesFromJson();
        LoadWordsByDifficulty();
        LoadNextWord();
    }

    void Update()
    {
        if (timerRunning)
        {
            timer += Time.deltaTime;
            timerText.text = "Время: " + timer.ToString("F1") + " сек";
        }

        gestureTimer += Time.deltaTime;
        if (gestureTimer >= gestureCheckCooldown)
        {
            TryRecognizeGesture();
            gestureTimer = 0f;
        }
    }

    void LoadPosesFromJson()
    {
        string path = Path.Combine(Application.temporaryCachePath, "default_poses_temp.json");
        if (!File.Exists(path))
        {
            Debug.LogError("Файл с позами не найден: " + path);
            return;
        }

        string json = File.ReadAllText(path);
        PoseDataSet dataset = JsonUtility.FromJson<PoseDataSet>(json);

        foreach (var namedPose in dataset.poses)
        {
            var jointDict = new Dictionary<HandJointId, Pose>();
            foreach (var jointData in namedPose.joints)
            {
                if (System.Enum.TryParse(jointData.jointId, out HandJointId id))
                {
                    jointDict[id] = jointData.pose.ToPose();
                }
            }
            loadedPoses[namedPose.poseName.ToUpper()] = jointDict;
        }

        Debug.Log("Загружено поз: " + loadedPoses.Count);
    }

    void LoadWordsByDifficulty()
    {
        string difficulty = PlayerPrefs.GetString("Difficulty", "Лёгкий");
        difficultyText.text = "Уровень: " + difficulty;

        // Очистка текущего списка слов
        currentWords.Clear();

        List<string> easy = new() { "ГЭС", "Урал", "Томь", "Лена", "Рим", "СПБ", "ВАЗ", "Анна", "ЗИЛ", "ГИП" };
        List<string> medium = new() { "Москва", "Тверь", "Ирина", "Омега", "Сибирь", "Арбат", "Каспий", "Саратов", "Самара" };
        List<string> hard = new() { "Саратов", "Красная", "Академия", "Политех", "Новгород", "Павелец", "Калинин", "Гойда" };


        List<string> source = difficulty switch
        {
            "Средний" => medium,
            "Тяжёлый" => hard,
            _ => easy
        };

        while (currentWords.Count < 3)
        {
            string word = source[Random.Range(0, source.Count)];
            if (!currentWords.Contains(word))
                currentWords.Add(word);
        }
    }


    void LoadNextWord()
    {
        if (currentWordIndex >= currentWords.Count)
        {
            wordText.text = "";
            inputText.text = "";
            ShowEndScreen(); // вызываем отдельную функцию завершения
            return;
        }

        currentWord = currentWords[currentWordIndex];
        currentInput = "";
        currentLetterIndex = 0;
        wordText.text = currentWord.ToUpper();
        UpdateInputDisplay();
    }

    void UpdateInputDisplay()
    {
        inputText.text = currentInput.ToUpper();
    }

    public void SkipLetter()
    {
        if (currentLetterIndex < currentWord.Length)
        {
            currentInput += currentWord[currentLetterIndex];
            skippedLetters++; // Увеличиваем счётчик пропущенных букв
            currentLetterIndex++;
            UpdateInputDisplay();
            if (currentLetterIndex >= currentWord.Length)
            {
                currentWordIndex++;
                Invoke(nameof(LoadNextWord), 1f);
            }
        }
    }


    public void SkipWord()
    {
        skippedWords++; // Увеличиваем счётчик пропущенных слов
        currentWordIndex++;
        Invoke(nameof(LoadNextWord), 0.5f);
    }

    void TryRecognizeGesture()
    {
        if (currentWordIndex >= currentWords.Count || currentLetterIndex >= currentWord.Length)
            return;

        if (!userHand.GetJointPose(HandJointId.HandPalm, out Pose palmPose)) return;

        foreach (var pose in loadedPoses)
        {
            if (IsMatchingPose(pose.Value, palmPose))
            {
                string recognized = pose.Key;
                string expected = currentWord[currentLetterIndex].ToString().ToUpper();

                if (recognized == expected)
                {
                    currentInput += recognized;
                    currentLetterIndex++;
                    UpdateInputDisplay();

                    if (currentLetterIndex >= currentWord.Length)
                    {
                        currentWordIndex++;
                        Invoke(nameof(LoadNextWord), 1f);
                    }
                }

                break;
            }
        }
    }
    void ShowEndScreen()
    {
        if (endPanel != null)
        {
            endPanel.SetActive(true);
            levelPanel.SetActive(false);

            finalTimeText.text = "Время: " + timer.ToString("F1") + " сек";
            skippedLettersText.text = "Пропущено букв: " + skippedLetters;
            skippedWordsText.text = "Пропущено слов: " + skippedWords;
        }

        timerRunning = false;
    }

    public void ReturnToMenu()
    {
        SceneManager.LoadScene("Scenes/Main Menu");
    }

    bool IsMatchingPose(Dictionary<HandJointId, Pose> saved, Pose palmPose)
    {
        foreach (var joint in trackedJoints)
        {
            if (!userHand.GetJointPose(joint, out Pose currentPose)) continue;
            if (!saved.TryGetValue(joint, out Pose savedPose)) continue;

            Vector3 localCurrentPos = Quaternion.Inverse(palmPose.rotation) * (currentPose.position - palmPose.position);
            Quaternion localCurrentRot = Quaternion.Inverse(palmPose.rotation) * currentPose.rotation;

            float posDiff = Vector3.Distance(localCurrentPos, savedPose.position);
            float rotDiff = Quaternion.Angle(localCurrentRot, savedPose.rotation);

            if (posDiff > posThreshold || rotDiff > rotThreshold)
                return false;
        }

        return true;
    }
}