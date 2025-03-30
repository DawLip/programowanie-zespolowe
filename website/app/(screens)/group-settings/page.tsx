"use client"
import { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';

import {Header, Aside, Icon, Section, UserCard, Message } from '../../components';

export default function GroupSettings() {
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
        <Header header={"Python lovers group"} name={"Adam"} surname={"Freineg"} backArrow/>
        <main className='gap-32 px-32 pb-32'>
          <section className='flex-col grow gap-32 p-32 rounded-[32] surface'>
            <div>Python Lovers Group</div>
            <LabeledContent label="About" content='Za Twoją zgodą, my i nasi partnerzy (881) używamy plików cookie lub podobnych technologii do przechowywania i przetwarzania danych osobowych oraz uzyskiwania dostępu do tych danych, takich jak informacje o Twojej wizycie na tej stronie internetowej, adresy IP i identyfikatory plików cookie. Niektórzy partnerzy nie proszą o zgodę' long />
            <LabeledContent label="Add user">X</LabeledContent>
            <LabeledContent label="Owner">
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
            </LabeledContent>
            <LabeledContent label="Admins">
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
            </LabeledContent>
            <LabeledContent label="Users">
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
              <ParticipantCard name={"John"} surname={"Brown"} isActive={true} />
            </LabeledContent>
          </section>
        </main>
      </div>
    </main>
  );
}

const ParticipantCard = ({name, surname, isActive}:{name: string, surname: string, isActive: boolean}) => (
  <UserCard name={"John"} surname={"Brown"} isActive={true} 
    buttons={
      <>
        <Icon src={"/icons/cross.png"} size={40} onClick={()=>{}} />
        <Icon src={"/icons/check.png"} size={40} onClick={()=>{}} />
        <Icon src={"/icons/check.png"} size={40} onClick={()=>{}} />
      </>
    }
  />
)

const LabeledContent = ({label, content, long, children}:{label: string, content?: string, long?: boolean, children?: any}) => (
  <div className='flex-col'>
    <span className='text-xl on_surface_light_gray font-bold'>{label}</span>
    {content && <p className={`on_surface_gray ${long?"text-xl":"text-[32px]"}`}>{content}</p>}
    {children}
  </div>
)
