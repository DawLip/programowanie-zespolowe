import { ProfileImage } from './';

const Message = ({ isUserAuthor, src, children }:{
  isUserAuthor: Boolean,
  src?: string,
  children: any
}) => (
  <div className={`justify-${isUserAuthor?"end":"start"} gap-16`}>
    { src && !isUserAuthor && <ProfileImage src={src} size={48} /> }
    <div 
      className={`p-16 rounded-[16] bg-[#D6D6D6] on_surface_gray`}
      style={isUserAuthor ? {borderEndEndRadius: 0} : {borderEndStartRadius: 0}}  
    >
      {children}
    </div>
    { src && isUserAuthor && <ProfileImage src={src} size={48} /> }
  </div>
)

export default Message