
class GlobalGameData
{
    public int difficultyCode = 0;
    public int[] cards;
    public int totolChampionType = 9;
    ///champions player choose
    public int[] chosenChampion = new int[20];


    private static GlobalGameData _instance = new GlobalGameData();
    public static GlobalGameData getInstance()
    {
        return _instance;
    }

    public static GlobalGameData initInstance()
    {
        _instance = new GlobalGameData();
        return _instance;
    }

    public void renewchosenChampionArray()
    {
        for (int i = 0; i < totolChampionType; i++)
        {
            chosenChampion[i] = 0;
        }
        /// aviod no card chosen
        if (cards.Length <= 0)
        {
            chosenChampion[0] = 1;
            chosenChampion[1] = 1;
            chosenChampion[2] = 1;
        }
        for (int i = 0; i < cards.Length; i++)
        {
            chosenChampion[cards[i]] = 1;
        }
    }
}
