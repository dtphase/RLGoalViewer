SetKeyDelay, 125

GoalNumber := 1
GoodGoals := ""

Gui, +LastFound -Caption +AlwaysOnTop
Gui, Add, Text, , Good goal?
Gui, Add, Button, xm gYes w40, Yes
Gui, Add, Button, x+10 gNo w40, No



ResetReplay()
{
    BlockInput, MouseMove
    MouseMove, 5,5
    Send {Escape}
    Send {Down}
    Send {Enter}
    Sleep, 200
    Send {Enter}
    BlockInput, MouseMoveOff
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
    FileReadLine, GameNumber, C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\active.txt, 2
    return GameNumber
}

GetVideoNumber() 
{
    FileReadLine, VideoNumber, C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\active.txt, 1
    return VideoNumber
}

GetNextGoalKeyframe() {
    global GoalNumber
    VideoNumber := GetVideoNumber()
    GameNumber := GetGameNumber()
    LineNumber := GameNumber + 1
    Path := "C:\Users\stream\Documents\My Games\Rocket League\TAGame\Demos\" VideoNumber "\Game" GameNumber ".txt"
    FileReadLine, Keyframe, %Path%, %LineNumber%
    ToolTip, %Keyframe%
    return Keyframe
}

NextGoal()
{
    ResetReplay()
    NextFrame := GetNextGoalKeyframe()
    if (NextFrame == 0) {
        return
    }
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
    Gui, Show, x5 y5
    MouseMove, 5,5
}



Yes()
{
    Gui, Hide   ;hides the window
    WinActivate, Rocket League
    global GoalNumber
    global GoodGoals
    GoalAdjust := GoalNumber - 1
    GoodGoals .= " " GoalAdjust
    NextGoal()
}

No()
{
    Gui, Hide
    NextGoal()
}


WatchAllGoals() 
{
    NextGoal()
}

#IfWinActive, Rocket League
{
    w::ResetReplay()

    s::SetCamera()
    
    d::NextGoal()

    e::GetNextGoalKeyframe()

    x::WatchAllGoals()

    q::Suspend
    return
}