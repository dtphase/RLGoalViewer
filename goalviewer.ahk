SetKeyDelay, 125

GoalNumber := 1

ResetReplay()
{
    Send {Escape}
    Send {Down}
    Send {Enter}
    Sleep, 50
    Send {Enter}
    return 0
}

SetCamera()
{
    Click, right
    Click, right
    Click, right
    Click, right
    Click, right
}

GetNextKeyframeInInterval(Keyframe)
{
    Interval := 5
    Multiplier := 0.03
    NumIntervals := Floor((Keyframe * Multiplier - 1) / Interval)
    return NumIntervals
    MsgBox, 4,, %NumIntervals%
}

GetLineFromFile(LineNum, Filename)
{
    FileReadLine, File, Filename, LineNum
    return File
}

GetGameNumber() 
{
    FileReadLine, GameNumber, C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\active.txt, 1
    return GameNumber
}

GetVideoNumber() 
{
    FileReadLine, VideoNumber, C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\active.txt, 2
    return VideoNumber
}

GetNextGoalKeyframe() {
    global GoalNumber
    VideoNumber := GetVideoNumber()
    GameNumber := GetGameNumber()
    Path := "C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\" VideoNumber "\Game" GameNumber ".txt"
    FileReadLine, Keyframe, %Path%, %GoalNumber%
    ToolTip, %Keyframe%
    return Keyframe
}

NextGoal()
{
    global GoalNumber
    ResetReplay()
    NextFrame := GetNextGoalKeyframe()
    ToolTip, %NextFrame%
    FastForwards := GetNextKeyframeInInterval(NextFrame) ; 410 is roughly 8 seconds
    Sleep, 2000
    SetCamera()
    ToolTip, %FastForwards%
    Loop, %FastForwards%
    {
        Send {Right}
    }
    GoalNumber += 1
}

MoveMsgBox()
{
	WinGetActiveTitle, Title
    WinMove, %Title%,, 0, 0
    return
}

WatchAllGoals() 
{
    NextGoal()
    GoodGoals := "G"
    Loop {
        global GoalNumber
        MsgBox, 4100,Title, Good goal? %GoodGoals%
        Sleep, 100
        MoveMsgBox()
        IfMsgBox Yes
        {
            GoalAdjust := GoalNumber - 1
            GoodGoals .= " "  GoalAdjust
        }
        NextGoal()
    }
}

#IfWinActive, Rocket League
{
    w::ResetReplay()

    s::SetCamera()
    
    d::NextGoal()

    e::GetNextGoalKeyframe()

    x::WatchAllGoals()
    return
}