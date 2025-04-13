"use client";

import React, { createContext, useContext, useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import Cookies from 'js-cookie';

interface SocketContextType {
  socket: Socket | null;
  isConnected: boolean;
}

const SocketContext = createContext<SocketContextType>({
  socket: null,
  isConnected: false,
});

export const SocketProvider = ({ children }: { children: React.ReactNode }) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const token = Cookies.get('token');
    if (!token) {
      console.warn("Brak tokenu — socket nie zostanie połączony.");
      return;
    }

    const newSocket = io("http://localhost:5000", {
      extraHeaders: {
        Authorization: `Bearer ${token}`,
      },
      autoConnect: true,
    });

    setSocket(newSocket);

    newSocket.on("connect", () => {
      console.log("✅ Socket połączony!");
      setIsConnected(true);
    });

    newSocket.on("disconnect", () => {
      console.log("❌ Socket rozłączony.");
      setIsConnected(false);
    });

    return () => {
      newSocket.disconnect();
    };
  }, []);

  return (
    <SocketContext.Provider value={{ socket, isConnected }}>
      {children}
    </SocketContext.Provider>
  );
};

export const useSocket = ():any => {
  const context = useContext(SocketContext);
  if (!context) {
    throw new Error("useSocket musi być używany wewnątrz <SocketProvider>");
  }
  return context;
};
