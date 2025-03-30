const Icon = ({src, size, onClick}:{src?: string, size: number, onClick: Function}) => (
  <img src={src==""?"/placeholder.png":src} style={{height:size, width: size}}/>
)

export default Icon