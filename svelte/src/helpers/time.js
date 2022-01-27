export function compareTime(start, end){
    const date1 = hoursAndMinutesToTime(start)
    const date2 = hoursAndMinutesToTime(end)
    return date1.getTime() < date2.getTime()
}

function weakCompareTime(start, end){
    const date1 = hoursAndMinutesToTime(start)
    const date2 = hoursAndMinutesToTime(end)
    return date1.getTime() <= date2.getTime()
}

export function isCurrentTimeBetween(start, end, current){
    console.log({start, end, current}, weakCompareTime(start, current) && weakCompareTime(current, end))
    return weakCompareTime(start, current) && weakCompareTime(current, end)
}

function hoursAndMinutesToTime(time){
    return new Date(`01/01/1970 ${time}`)
}

export function validateTimeDayJS(dayjsObj){

}

