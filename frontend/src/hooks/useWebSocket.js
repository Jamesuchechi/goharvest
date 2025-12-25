import { useEffect, useRef, useState } from 'react';

export function useWebSocket({ onMessage, onConnect, onDisconnect }) {
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/';

    ws.current = new WebSocket(WS_URL);

    ws.current.onopen = () => {
      setIsConnected(true);
      onConnect?.();
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      onDisconnect?.();
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage?.(data);
    };

    return () => {
      ws.current?.close();
    };
  }, []);

  const sendMessage = (data) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data));
    }
  };

  return { isConnected, sendMessage };
}
