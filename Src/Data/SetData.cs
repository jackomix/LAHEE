using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace LAHEE.Data;

public enum SetType {
    core,
    bonus,
    specialty,
    exclusive
}

public class SetData {
    public string Title;

    [JsonConverter(typeof(StringEnumConverter))]
    public SetType Type;

    [JsonProperty("ID")]
    public int AchievementSetId;

    // We send both casing variations to ensure RetroArch compatibility
    [JsonProperty("GameID")]
    public uint GameID;

    [JsonProperty("GameId")]
    public uint GameId => GameID;

    [JsonProperty("ImageIconURL")]
    public string ImageIconURL;

    [JsonProperty("ImageIconUrl")]
    public string ImageIconUrl => ImageIconURL;

    public List<AchievementData> Achievements;
    public List<LeaderboardData> Leaderboards;
    [JsonIgnore] public string FileSource;
}
