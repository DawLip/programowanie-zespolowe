"use client"
import { use, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation'
import { TextInput } from '../../../../components';
import Cookies from 'js-cookie';
import config from "../../../../config"

import {Header, Aside, Icon, Section, UserCard, Message } from '../../../../components';

export default function GroupSettings({ params }: { params: Promise<{ groupId: string }> }) {
  const { groupId } = use(params);
  const router = useRouter();
  
  const userId = Cookies.get('userId');
  
  const [group, setGroup] = useState<any>({});
  const [newDescription, setnewDescription] = useState("");
  const [newName, setnewName] = useState("");
  const [newMember, setnewMember] = useState("");
  const [potentialMembers, setPotentialMembers] = useState<any>([]);

  const userRole = group.members && group.members.find((m:any) => m.id === userId)?.role;

  const fetchGroupInfo = () => {
    fetch(`${config.api}/group/${groupId}`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log(response);
        setnewDescription(response.description || "");
        setnewName(response.name || "");
        setGroup(response);
      })
      .catch(error => console.error('Błąd:', error));
  }

  useEffect(() => { fetchGroupInfo() }, [])

  const removeMember = (id: string) => {
    fetch(`${config.api}/api/rooms/${groupId}/remove-member`, {
      headers: {
        "Authorization": `Bearer ${Cookies.get('token')}`,
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify({
        user_id: id
      })
    })
      .then(response => response.json())
      .then((response:any) => {
        fetchGroupInfo();
      })
      .catch(error => console.error('Błąd:', error));
  }

  const searchUsers = (e: any) => {
    setnewMember(e.target.value);
    fetch(`${config.api}/user/search?query=${e.target.value}`)
    .then(response => response.json())
    .then((response:any) => {
      setPotentialMembers(response.users);
    })
    .catch(error => console.error('Błąd:', error));
  }

  const addToGroup = (id: number) => {
    fetch(`${config.api}/api/rooms/${groupId}/add-member`, {
      headers: {
        "Authorization": `Bearer ${Cookies.get('token')}`,
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify({
        user_id: id
      })
    })
      .then(response => response.json())
      .then((response:any) => {
        fetchGroupInfo();
        setPotentialMembers([]);
        setnewMember("");
      })
      .catch(error => console.error('Błąd:', error));
  }

  const saveChanges = () => {
    fetch(`${config.api}/api/rooms/${groupId}/save-changes`, {
      headers: {
        "Authorization": `Bearer ${Cookies.get('token')}`,
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify({
        name: newName,
        description: newDescription
      })
    })
      .then(response => response.json())
      .then((response:any) => {
        fetchGroupInfo();
      })
      .catch(error => console.error('Błąd:', error));
  }

  const setRole = (id: string, role: string) => {
    fetch(`${config.api}/api/rooms/${groupId}/change-role`, {
      headers: {
        "Authorization": `Bearer ${Cookies.get('token')}`,
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify({
        user_id: id,
        new_role: role
      })
    })
      .then(response => response.json())
      .then((response:any) => {
        fetchGroupInfo();
      })
      .catch(error => console.error('Błąd:', error));
    }

  return (
    <>
      <Header header={`${newName || "Your group" } settings`} backArrow/>
      <main className='gap-32 px-32 pb-32'>
        <section className='flex-col grow gap-32 p-32 rounded-[32] surface'>
          <LineInput
            value={newName} 
            setValue={setnewName} 
            placeholder="Set group name"
          />
          {userRole != "USER" && <div className={"cursor-pointer"} onClick={saveChanges}>Save changes</div>}
          <TextInput 
            label="About" 
            value={newDescription} 
            placeholder="Write something about your group"
            setValue={setnewDescription}
            long 
          />
          {userRole != "USER" &&  <LabeledContent label="Add user">
            <div>
              <input type="text"
                value={newMember}
                onChange={e=>searchUsers(e)}
                placeholder="Add user to group"
                className='rounded-full px-16 py-8 text-xl border-2 border-solid border-gray-300'
              />
            </div>
            <div>
              { potentialMembers && potentialMembers.map((m:any) => (
                <UserCard 
                  name={m.name} 
                  surname={m.surname} 
                  isActive={m.isActive} 
                  buttons={<Icon src={"/icons/check.png"} size={40} onClick={()=>addToGroup(m.id)} />}
                />
              ))}
            </div>
          </LabeledContent>}
          <LabeledContent label="Owner">
            {group.members && group.members.filter((m:any) => m.role === "OWNER").map((m:any) => (
              <ParticipantCard 
                id={m.id}
                name={m.name} 
                surname={m.surname} 
                isActive={m.isActive}
                role={m.role} 
                removeMember={removeMember}
                setRole={setRole}
                userRole={userRole}
              />
            ))}
          </LabeledContent>
          <LabeledContent label="Admins">
          {group.members && group.members.filter((m:any) => m.role === "ADMIN").map((m:any) => (
              <ParticipantCard 
                id={m.id}
                name={m.name} 
                surname={m.surname} 
                isActive={m.isActive}
                role={m.role} 
                removeMember={removeMember}
                setRole={setRole}
                userRole={userRole}
              />
            ))}
          </LabeledContent>
          <LabeledContent label="Users">
            {group.members && group.members.filter((m:any) => m.role === "USER").map((m:any) => (
              <ParticipantCard 
                id={m.id}
                name={m.name} 
                surname={m.surname} 
                isActive={m.isActive}
                role={m.role} 
                removeMember={removeMember}
                setRole={setRole}
                userRole={userRole}
              />
            ))}
          </LabeledContent>
        </section>
      </main>
    </>
  );
}

const ParticipantCard = ({name, surname, isActive, role, id, removeMember,setRole, userRole}:any) => (
  <UserCard name={name} surname={surname} isActive={isActive} 
    buttons={
      <>
        { role!="OWNER" && userRole!="USER" && <>
            <Icon src={"/icons/cross.png"} size={40} onClick={()=>removeMember(id)} />
            <Icon src={"/icons/check.png"} size={40} onClick={()=>setRole(id, role=="ADMIN"?"USER":"ADMIN")} />
          </>
        }
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

const LineInput = ({value, placeholder, setValue}:{value: string, placeholder: string, setValue: Function}) => {
  const spanRef = useRef<HTMLSpanElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { if (spanRef.current && inputRef.current) inputRef.current.style.width = `${spanRef.current.offsetWidth + 10}px`; }, [value]);

  return (
  <>
    <input 
      type="text" 
      ref={inputRef}
      value={value} 
      onChange={e=>setValue(e.target.value)} 
      placeholder={placeholder}
      className='flex shrink text-5xl on_surface_gray'
      style={{ width: `${value.length}ch` }}
    />
    <span ref={spanRef} className="absolute invisible text-5xl">{value || placeholder}</span>
  </>
)}