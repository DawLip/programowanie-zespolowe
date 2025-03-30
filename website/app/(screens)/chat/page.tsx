"use client"
import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';

import {Header, Aside, Icon, Section, UserCard, Message } from '../../components';

export default function ChatPage() {
  const router = useRouter();

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const u = { id: 0, name: 'John', surname:'Doe', lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const g = { id: 0, name: "Python lovers", lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const users = [u,u,u];
  const groups = [g,g,g];

  const chatRef:any = useRef(null);

  useEffect(() => { if(chatRef.current) chatRef.current.scrollTop = chatRef.current.scrollHeight; }, [messages]);
  useEffect(() => { if(!Cookies.get('token')) router.push('/login') },[] )

  return (
    <main className='max-h-screen'>
      <Aside users={users} groups={groups} />
      <div className='flex-col grow pb-32'>
        <Header header={"Frank Drey"} name={"Adam"} surname={"Freineg"} backArrow />
        <main className='gap-32 px-32'>
          <section className='flex-1 flex-col gap-16'>
            <div 
              ref={chatRef} 
              className='flex-col gap-32 p-32 overflow-y-scroll scrollbar-none surface rounded-[32] bottom-0' 
              style={{height: 'calc(100vh - 96px - 64px - 32px)'}}
            >
              <Message isUserAuthor={true} src="">Hey, whats up?</Message>
              <Message isUserAuthor={false}>Hey, whats up?</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={false}>Hey, whats up?</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={false}>Hey, whats up?</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={false}>Hey, whats up?</Message>
              <Message isUserAuthor={true} src="d">Hey, whats up?</Message>
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
                John Brown
              </span>
              <div className='gap-16'>
                <Icon src={""} size={48} onClick={()=>{}}/>
                <Icon src={""} size={48} onClick={()=>{}}/>
                <Icon src={""} size={48} onClick={()=>{}}/>
              </div>
            </div>
            <div className='flex-col gap-16'>
              <LabeledContent label="About me" content={"Za Twoją zgodą, my i nasi partnerzy (881) używamy plików cookie lub podobnych technologii do przechowywania i przetwarzania danych osobowych oraz uzyskiwania dostępu do tych danych, takich jak informacje o Twojej wizycie na tej stronie internetowej, adresy IP i identyfikatory plików cookie. Niektórzy partnerzy nie proszą o zgodę"} long/>
              <LabeledContent label="Email" content={"john.brown@gmail.com"}/>
              <LabeledContent label="Phone" content={"+48 562 038 367"}/>
              <LabeledContent label="Address" content={"Katowice, Krakowska 73a"}/>
            </div>
          </section>
        </main>
      </div>
    </main>
  );
}

const LabeledContent = ({label, content, long}:{label: string, content: string, long?: boolean}) => (
  <div className='flex-col'>
    <span className='text-xl on_surface_light_gray font-bold'>{label}</span>
    <p className={`on_surface_gray ${long?"text-xl":"text-[32px]"}`}>{content}</p>
  </div>
)
