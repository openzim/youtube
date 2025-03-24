import Component from 'video.js/dist/types/component'

export default interface TimeTooltip extends Component {
  update: (seekBarRect: DOMRect, seekBarPoint: number, time: string) => void
  write: (text: string) => void
}
