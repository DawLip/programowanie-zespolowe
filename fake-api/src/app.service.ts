import { Injectable } from '@nestjs/common';

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
}
