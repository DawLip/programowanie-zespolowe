"use Client"

const Icon = ({src, size, onClick}:{src?: string, size: number, onClick: ()=>void}) => (
  <img 
    src={src==""?"/placeholder.png":src} 
    style={{height:size, width: size}} 
    onClick={onClick}
  />
)

export default Icon