import React, { useState, useEffect } from 'react';
import './Standings.css';

const PlayersTable = () => {
    const [players, setPlayers] = useState([]);
    const [sortedPlayers, setSortedPlayers] = useState([]);
    const [sortKey, setSortKey] = useState(null);
    const [sortOrder, setSortOrder] = useState('asc');

    useEffect(() => {
        fetch('/api/players')
            .then(response => response.json())
            .then(data => setPlayers(data))
            .catch(error => console.error('Error fetching players:', error));
    }, []);

    useEffect(() => {
        // Sort players when sortKey or sortOrder changes
        const sortPlayers = () => {
            const sorted = Object.keys(players).sort((a, b) => {
                const playerA = players[a];
                const playerB = players[b];
    
                // Implement sorting logic based on sortKey and sortOrder
                switch (sortKey) {
                    case 'Name':
                        // Implement sorting based on name
                        return sortOrder === 'asc' ? playerA.last_name.localeCompare(playerB.last_name) : playerB.last_name.localeCompare(playerA.last_name);
                    case 'Correct Tips':
                        // Implement sorting based on correct tips
                        return sortOrder === 'asc' ? playerA.correct_tips - playerB.correct_tips : playerB.correct_tips - playerA.correct_tips;
                    case 'Bonus Points':
                        // Implement sorting based on bonus points
                        return sortOrder === 'asc' ? playerA.bonus_points - playerB.bonus_points : playerB.bonus_points - playerA.bonus_points;
                    case 'Points':
                        // Implement sorting based on points tally
                        return sortOrder === 'asc' ? playerA.points_tally - playerB.points_tally : playerB.points_tally - playerA.points_tally;
                    default:
                        return 0;
                }
            });
            setSortedPlayers(sorted);
        };
        
        sortPlayers(); // Initial sorting
    }, [players, sortKey, sortOrder]);
    
    // Function to handle header click and update sortKey and sortOrder
    const handleSort = (key) => {
        if (sortKey === key) {
            // Toggle sort order if the same column header is clicked
            setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
        } else {
            // Set new sort key and default to ascending order
            setSortKey(key);
            setSortOrder('asc');
        }
        console.log(sortOrder)
    };

    return (
        <div>
            <table className="standings-table">
                <thead>
                    <tr>
                        <th onClick={() => handleSort('Name')}>Tipster</th>
                        <th onClick={() => handleSort('Points')}>Points</th>
                        <th onClick={() => handleSort('Bonus Points')}>Bonus Points</th>
                        <th onClick={() => handleSort('Correct Tips')}>Correct Tips</th>
                    </tr>
                </thead>
                <tbody>
                    {sortedPlayers.map(playerId => {
                        const player = players[playerId];
                        return (
                            <tr key={playerId}>
                                <td>{player.last_name}, {player.first_name}</td>
                                <td>{player.points_tally.toFixed(2)}</td>
                                <td>{player.bonus_points}</td>
                                <td>{player.correct_tips}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default PlayersTable;
