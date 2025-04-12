"use client"
import { useEffect, useRef, useState } from 'react';
import { useRouter, useParams } from 'next/navigation'
import Cookies from 'js-cookie';
import config from "../../../../../config"

import {Header, Aside, Icon, Section, UserCard, Message } from '../../../../../components';

export default function ChatPage() {
  const router = useRouter();
  const params = useParams();

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [correspondent, setCorrespondent] = useState<any>({});

  const userId = Cookies.get('userId');

  const chatRef:any = useRef(null);

  useEffect(() => { if(chatRef.current) chatRef.current.scrollTop = chatRef.current.scrollHeight; }, [messages]);
  useEffect(() => { 
    fetch(`${config.api}/${params.chatType=="private"?"user":"group"}/${params.id}`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log("/group/${params.id}", response)
        setCorrespondent(response);
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
  return (
    <>
      <Header 
        header={params.chatType=="private" ? `${correspondent.name} ${correspondent.surname}` : correspondent.name} 
        backArrow 
        userProfileSrc=' '
      />
      <main className='gap-32 px-32'>
        <section className='flex-1 flex-col gap-16'>
          <div 
            ref={chatRef} 
            className='flex-col gap-32 p-32 overflow-y-scroll scrollbar-none surface rounded-[32] bottom-0 justify-end' 
            style={{height: 'calc(100vh - 96px - 64px - 32px)'}}
          >
            {messages && messages.map((m:any)=>(
              <Message isUserAuthor={m.user_id==userId} src="">{m.message}</Message>
            ))}
          </div>
          <div className='items-center h-64 px-32 surface rounded-[32]'>
            <input 
              type="text" 
              value={message} 
              placeholder='Write Something...'
              onChange={e=>setMessage(e.target.value)}
              className='flex grow text-2xl on_surface_gray .placeholder-[#A0A0A0]'
            />
            <Icon src={"/icons/send.png"} size={32} onClick={()=>{}}/>
          </div>
        </section>
        <section 
          className='flex-1 flex-col grow gap-32 p-32 surface rounded-[32] overflow-y-scroll scrollbar-none'
          style={{height: 'calc(100vh - 96px)'}}
        >
          <div className='justify-between'>
            <span className='text-5xl on_surface_gray font-normal'>
              {correspondent.name} {correspondent.surname}
            </span>
            <div className='gap-16'>
              <Icon src={"/icons/facebook.png"} size={48} onClick={()=>{}}/>
              <Icon src={"/icons/instagram.png"} size={48} onClick={()=>{}}/>
              <Icon src={"/icons/linkedin.png"} size={48} onClick={()=>{}}/>
            </div>
          </div>
          <div className='flex-col gap-16'>
            {correspondent.destription && <LabeledContent label="About me" content={correspondent.destription} long/>}
            {correspondent.email && <LabeledContent label="Email" content={correspondent.email}/>}
            {correspondent.phone && <LabeledContent label="Phone" content={correspondent.phone}/>}
            {correspondent.address && <LabeledContent label="Address" content={correspondent.address}/>}
          </div>
        </section>
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
