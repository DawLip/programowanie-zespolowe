import { use } from 'react';
import Aside from './components/Aside';

export default function Home() {
  const u = { id: 0, name: 'John', surname:'Doe', lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const g = { id: 0, name: "Python lovers", lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const users = [u,u,u];
  const groups = [g,g,g];
  
  return (
    <main>
      <Aside users={users} groups={groups}/>
    </main>
  );
}
