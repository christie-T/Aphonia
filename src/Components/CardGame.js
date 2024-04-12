import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000'); // Assuming your server runs on localhost:5000

function CardGame() {
  const [lobbyPlayers, setLobbyPlayers] = useState([]);
  const [playerCards, setPlayerCards] = useState({});

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to server');
    });

    socket.on('disconnect', () => {
      console.log('Disconnected from server');
    });

    socket.on('lobby_update', (players) => {
      setLobbyPlayers(players);
    });

    socket.on('match_found', ({ player_cards }) => {
      setPlayerCards(player_cards);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleJoinLobby = () => {
    console.log('Joining lobby...');
    socket.emit('join_lobby');
  };

  const handleStartGame = () => {
    socket.emit('start_game');
  };

  return (
    <div>
      <h1>Card Game</h1>
      <div>
        <button onClick={handleJoinLobby}>Join Lobby</button>
        <button onClick={handleStartGame}>Start Game</button>
      </div>
      <div>
        <h2>Lobby Players</h2>
        <ul>
          {lobbyPlayers.map((player, index) => (
            <li key={index}>{player}</li>
          ))}
        </ul>
      </div>
      <div>
        <h2>Player Cards</h2>
        <ul>
          {Object.entries(playerCards).map(([player, cardFace]) => (
            <li key={player}>
              {player}: {cardFace}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default CardGame;