"use client"
import { useEffect, useRef, useState } from 'react';
import { useRouter, useParams } from 'next/navigation'
import Cookies from 'js-cookie';
import { useSocket } from '../../../../../socket';
import config from "../../../../../config"

import {Header, Aside, Icon, Section, UserCard, Message } from '../../../../../components';

export default function ChatPage(props:any) {
  const router = useRouter();
  const params = useParams();
  const { socket, isConnected } = useSocket();

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [correspondent, setCorrespondent] = useState<any>({});
  const [isShowInfo, setIsShowInfo] = useState(false);

  const userId = Cookies.get('userId');

  const chatRef:any = useRef(null);

  useEffect(() => { if(chatRef.current) chatRef.current.scrollTop = chatRef.current.scrollHeight; }, [messages]);
  useEffect(() => { 
    fetch(`${config.api}/group/${params.id}`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((group:any) => {
        console.log("/group/${params.id}", group);
        if(group.type=="GROUP") setCorrespondent(group);
        else {
          setCorrespondent(group.members.find((m:any) => m.id!=userId));
        }
      })
      .catch(error => console.error('Błąd:', error));
   },[] )
   useEffect(() => { 
    fetch(`${config.api}/api/rooms/${params.id}/messages`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log("/api/rooms/${params.id}/messages", response)
        setMessages(response);
      })
      .catch(error => console.error('Błąd:', error));
   },[] )
  useEffect(() => {
    if(!isConnected) return;
    socket.emit("join_room", {rooms: [params.id]});
    socket.on("join_room_response", (res:any) => {
      console.log("join_room_response", res)
    });

    socket.on("new_message", (message:any) => {
      console.log("new_message", message)
      if(message.group_id!=params.id) return;
      if(message.message_id==messages[messages.length-1].message_id) return;
      setMessages((prev:any) => [...prev, message]);
    });
  }, [socket, isConnected]);

  const sendMessage = () => {
    if(!message) return;
    socket.emit("send_message", {
      room: params.id,
      message: message
    });
    setMessage("");
  }

  return (
    <>
      <Header 
        header={<>
          {params.chatType=="private" ? `${correspondent.name} ${correspondent.surname}` : correspondent.name} 
          <>
            <Icon 
            src={"/icons/info.png"} 
            size={32} 
            onClick={()=>setIsShowInfo(prev=>!prev)}/>
            {params.chatType=="GROUP"
            &&  <Icon 
                  src={"/icons/settings.png"} 
                  size={32} 
                  onClick={()=>router.push(`/group-settings/${params.id}`)}/>
            }
          </>
        </>} 
        backArrow 
        userProfileSrc=' '
      />
      <main className='gap-32 px-32'>
        <section 
          className='flex-1 flex-col gap-16'
        >
          <div 
            ref={chatRef} 
            className='flex-col gap-16 overflow-y-scroll scrollbar-none'
            style={{height: 'calc(100vh - 96px - 64px - 32px - 16px)'}}
          >
            <div className='flex-col min-h-full gap-4 p-32 surface rounded-[32] bottom-0 justify-end'>
            
              {messages[0] && messages.map((m:any, i:number)=>(
                <Message 
                  key={m.message_id}
                  isFirst={(messages[i-1] && (messages[i-1].name!=m.name))||i==0}
                  isLast={(messages[i+1] && (messages[i+1].name!=m.name))||i+1==messages.length}
                  name={m.name}
                  isUserAuthor={m.user_id==userId} 
                  src="/icons/add-friend.png"
                >
                  {m.message}
                </Message>
              ))}
            </div>
          </div>
          <div className='items-center h-64 px-32 surface rounded-[32]'>
            <input 
              type="text" 
              value={message} 
              placeholder='Write Something...'
              onChange={e=>setMessage(e.target.value)}
              className='flex grow text-2xl on_surface_gray .placeholder-[#A0A0A0]'
            />
            <Icon src={"/icons/send.png"} size={32} onClick={sendMessage}/>
          </div>
        </section>
        {isShowInfo && <section 
          className='flex-1 flex-col grow gap-32 p-32 surface rounded-[32] overflow-y-scroll scrollbar-none'
          style={{}}
        >
          <div className='justify-between'>
            <span className='text-5xl on_surface_gray font-normal'>
              {correspondent.name} {correspondent.surname}
            </span>
            <div className='gap-16'>
              {correspondent.facebook && <Icon src={"/icons/facebook.png"} size={48} onClick={()=>{}}/>}
              {correspondent.instagram && <Icon src={"/icons/instagram.png"} size={48} onClick={()=>{}}/>}
              {correspondent.linkedin && <Icon src={"/icons/linkedin.png"} size={48} onClick={()=>{}}/>}
            </div>
          </div>
          <div className='flex-col gap-16'>
            {correspondent.description && <LabeledContent label="About" content={correspondent.description} long/>}
            {correspondent.email && <LabeledContent label="Email" content={correspondent.email}/>}
            {correspondent.phone && <LabeledContent label="Phone" content={correspondent.phone}/>}
            {correspondent.address && <LabeledContent label="Address" content={correspondent.address}/>}
          </div>
        </section>}
      </main>
    </>
  );
}

const LabeledContent = ({label, content, long}:{label: string, content: string, long?: boolean}) => (
  <div className='flex-col'>
    <span className='text-xl on_surface_light_gray font-bold'>{label}</span>
    <p className={`on_surface_gray ${long?"text-xl":"text-[32px]"}`}>{content}</p>
  </div>
)
