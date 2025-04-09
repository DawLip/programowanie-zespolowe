import { ProfileImage } from './';

const Message = ({ isUserAuthor, src, children }:{
  isUserAuthor: Boolean,
  src?: string,
  children: any
}) => (
  <div className={`justify-${isUserAuthor?"end":"start"} gap-16 items-end`}>
    { src && !isUserAuthor && <ProfileImage src={src} size={48} /> }
    <div 
      className={`px-24 py-8 rounded-[16] msg white text-xl font-light`}
      style={isUserAuthor ? {borderEndEndRadius: 0} : {borderEndStartRadius: 0}}  
    >
      {children}
    </div>
    { src && isUserAuthor && <ProfileImage src={src} size={48} /> }
  </div>
)

export default Message