import { Injectable, Param } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Hello World!';
  }
  getDashboard(): any {
    const invitation = {
      id: 0,
      name: "John",
      surname: "Doe",
      isActive: true
    }
    const message = {
      messageAuthor: "you", 
      message: "hey :D"
   }
    const lastChat = {
      userId: 0,
      name: "John",
      surname: "Doe",
      messages: [message,message,message],
      isActive: true
    }
    const group = {
      groupId: 0,
      name: "Python lovers",
      messages: [message,message,message],
      isActive: true
    }
    const mayK = {
      id: 0,
      name: "John",
      surname: "Doe",
      isActive: true
    }
    return ({
      invitations: [invitation,invitation],    
      lastChats: [lastChat,lastChat,lastChat,lastChat,lastChat,lastChat],
      groups: [group,group,group,group,group,group],
      mayKnow: [mayK,mayK,mayK,mayK,mayK,mayK,mayK,mayK,mayK,mayK,mayK,mayK]
    });
  }
  getAside(): any {
    const friend = {
      name: "John",
      surname: "Doe",
      lastMessage: "hey :D",
      lastMessageAuthor: "you",
      isActive: true
    }
    const group = {
      name: "Python lovers",
      lastMessage: "Hey :D",
      lastMessageAuthor: "you",
      isActive: true
    }
  
    return ({
      friends: [friend,friend,friend,friend,friend,friend],
      groups: [group,group,group,group]
    })
  }

  getSearch(query): any {
    const length = Math.floor(Math.random() * (8 - 3 + 1)) + 3;
    const queryRes = {
      id: 0,
      name: "John",
      surname: "Doe",
      type: "user"
    }
    return Array.from({ length: length }, (_, i) => queryRes);
  }

  getGroup():any {
    const user = {
      id: 0,
      name: "John",
      surname: "Doe",
    }
    return {
      id: 0,
      type: "group",
      name: "Python lovers",
      about:"Python lovers group",
      users: [user,user,user,user,user,user,user,user,user,user,user],
      admins: [user,user,user,user],
      owner: user
    }
  }
}
