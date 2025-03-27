"use client"
import { useState } from 'react'

import c from '../colors'
function UserCard({user}){
  return (
    <div className="gap-8">
      <div className="bg-black rounded-full size-40 items-end justify-end">
        {user.isActive && <div className="bg-green-400 rounded-full size-16"></div>}
      </div>
      <div className="flex-col gap-4 text-base/19">
        <div className="on_surface_gray font-semibold">
          {user.name}: {user.surname}
        </div>
        <div className="on_surface_light_gray">
          {user.lastMessageAuthor} {user.lastMessage}
        </div>
      </div>
    </div>
  )
}

function FriendsGroupButton({callback, label, checked}){
  return (
    <button 
      onClick={()=>callback(label==="Friends")} 
      className={`grow on_surface_gray py-8 ${checked && `border-b-1 border-[${c.border}]`}`}
    >
      {label}
    </button>
  )
}

export default function Home({ users, groups }) {
  const [friendsOrGroups, setFriendsOrGroups] = useState(true)
  return (
    <aside className="w-256 h-screen flex-col gap-16 p-16 surface">
      <header className="on_surface_gray text-3xl font-bold justify-center">ChatNow</header>
      <section className="flex-col gap-16">
        <div>
          <FriendsGroupButton label ="Friends" callback={setFriendsOrGroups} checked={friendsOrGroups}/>
          <FriendsGroupButton label ="Groups" callback={setFriendsOrGroups} checked={!friendsOrGroups}/>
        </div>
        <div className="flex-col gap-16">
          {users.map(u => (<UserCard user={u}/>))}
        </div>
      </section>
    </aside>
  );
}
