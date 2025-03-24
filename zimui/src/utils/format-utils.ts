import dayjs from 'dayjs'
import duration from 'dayjs/plugin/duration'

dayjs.extend(duration)

export const formatTimestamp = (isoDuration: string): string => {
  // Parse the ISO 8601 duration string
  const parsedDuration = dayjs.duration(isoDuration)

  // Extract hours, minutes, and seconds
  const hours = parsedDuration.hours()
  const minutes = parsedDuration.minutes()
  const seconds = parsedDuration.seconds()

  // Format the timestamp
  let formattedTimestamp: string
  const formattedHours = String(hours).padStart(2, '0')
  const formattedMinutes = String(minutes).padStart(2, '0')
  const formattedSeconds = String(seconds).padStart(2, '0')
  if (hours > 0) {
    formattedTimestamp = `${formattedHours}:${formattedMinutes}:${formattedSeconds}`
  } else {
    formattedTimestamp = `${formattedMinutes}:${formattedSeconds}`
  }

  return formattedTimestamp
}

export const formatDate = (date: string, format: string = 'MMM D, YYYY'): string => {
  return dayjs(date).format(format)
}

export const truncateText = (text: string, maxLength: number): string => {
  if (text.length > maxLength) {
    return `${text.slice(0, maxLength)}...`
  }
  return text
}

export const timeToSeconds = (timestr: string) => {
  const parts = timestr.split(':').map(Number)
  let seconds = 0

  if (parts.length === 3) {
    seconds = parts[0] * 3600 + parts[1] * 60 + parts[2]
  } else if (parts.length === 2) {
    seconds = parts[0] * 60 + parts[1]
  } else if (parts.length === 1) {
    seconds = parts[0]
  }

  return seconds
}
