"use Client"

const Icon = ({src, size, onClick}:{src?: string, size: number, onClick: ()=>void}) => (
  <img 
    src={src==""?"/placeholder.png":src} 
    style={{height:size, width: size}} 
    className="hover:cursor-pointer"
    onClick={onClick}
  />
)

export default Icon