import React, { useState, useEffect } from 'react';
import './Selections.css';

const Selections = () => {
    const [players, setPlayers] = useState([]);
    const [numberOfEvents, setNumberOfEvents] = useState(0);

    useEffect(() => {
        fetch('/api/players')
            .then(response => response.json())
            .then(data => {
                // Convert object of players to array
                const playerArray = Object.values(data);
                setPlayers(playerArray);

                // Calculate the maximum number of events
                const maxEvents = Math.max(...playerArray.map(player => {
                    const events = Object.keys(player).filter(key => key.startsWith('Event_'));
                    return events.length;
                }));
                setNumberOfEvents(maxEvents);
            })
            .catch(error => console.error('Error fetching players:', error));
    }, []);

    return (
        <div className="selections-table-container">
            <table className="selections-table">
                <thead>
                    <tr>
                        <th>Event</th>
                        {players.map(player => (
                            <th key={player.first_name}>{player.first_name} {player.last_name}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {[...Array(numberOfEvents)].map((_, index) => {
                        const eventNumber = index + 1;
                        return (
                            <tr key={index}>
                                <td>{eventNumber}</td>
                                {players.map(player => {
                                    const eventKey = `Event_${eventNumber}`;
                                    const event = player[eventKey];
                                    return (
                                        <td key={`${player.first_name}_${index}`}>
                                            {event ? (
                                                <>
                                                    {event.Selection}
                                                    {event.Bonus !== null && (
                                                        <>
                                                            {' '}
                                                            [{event.Bonus}]
                                                        </>
                                                    )}
                                                </>
                                            ) : (
                                                '-'
                                            )}
                                        </td>
                                    );
                                })}
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default Selections;
