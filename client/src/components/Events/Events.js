import React, { useState, useEffect } from 'react';
import './Events.css';

const Events =() => {

    const [events, setEvents] = useState([]);

    useEffect(() => {
        fetch('/api/events')
            .then(response => response.json())
            .then(eventsdata => setEvents(eventsdata))
            .catch(error => console.error('Error fetching events:', error));
    }, []);

    console.log(events)

    return (
        <div>
            <table className="events-table">
                <thead>
                    <tr>
                        <th className="column-id">ID</th>
                        <th className="column-event">Event</th>
                        <th className="column-result">Result</th>
                        <th className="column-bonus">Bonus Result</th>
                        <th className="column-tips">Tips</th>
                        <th className="column-Pts">Point Share</th>
                    </tr>
                </thead>
                <tbody>
                    {events.map(event => (                        
                        <tr key={event.Event_ID}>
                            <td className="column-id">{event.Event_ID.replace('Event_', '')}</td>
                            <td className="column-event">{event.Event}</td>
                            <td className="column-result">{event.Result}</td>
                            <td className="column-bonus">{event.Bonus || ''}</td>
                            <td className="column-tips">{event.Correct_Tips}</td>
                            <td className="column-Pts">{event.Point_Share.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )

}

export default Events;