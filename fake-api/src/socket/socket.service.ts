import { Injectable } from '@nestjs/common';
import { log } from 'console';
import { Socket } from 'socket.io';

@Injectable()
export class SocketService {
  private readonly connectedClients: Map<string, Socket> = new Map();

  handleConnection(socket: Socket): void {
    const clientId = socket.id;
    this.connectedClients.set(clientId, socket);
    socket.on('join', data=>{
      socket.join(data.room)
    })
    socket.on('message', data => {
      data = JSON.parse(data)

      console.log("message");
      console.log(data)
      socket.to(data.room).emit('message', { hello : "hi there", data})
    })
    socket.on('disconnect', () => {
      this.connectedClients.delete(clientId);
    });

    // Handle other events and messages from the client
  }

  // Add more methods for handling events, messages, etc.
}