import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import './Dashboard.css';

export default function Dashboard() {
  const [triggers, setTriggers] = useState([]);
  const [templates, setTemplates] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const triggersRes = await api.get('/api/triggers/');
      setTriggers(triggersRes.data);
      
      const templatesMap = {};
      for (let trigger of triggersRes.data) {
        const tempRes = await api.get(`/api/templates/?trigger_id=${trigger._id}`);
        templatesMap[trigger._id] = tempRes.data;
      }
      setTemplates(templatesMap);
    } catch (err) {
      if (err.response && err.response.status === 401) {
        navigate('/login');
      }
    }
  };

  const getTemplateForChannel = (triggerId, channel) => {
    const triggerTemplates = templates[triggerId] || [];
    return triggerTemplates.find(t => t.channel === channel);
  };

  const handleEdit = (triggerId, channel) => {
    // Basic prompt for demonstration. In real app, open a modal.
    const template = getTemplateForChannel(triggerId, channel);
    const body = prompt(`Enter new template body for ${channel}:`, template ? template.body : '');
    
    if (body !== null) {
      api.post('/api/templates/', {
        trigger_id: triggerId,
        channel: channel,
        body: body,
        title: "Notification",
        subject: "Notification",
        is_enabled: true
      }).then(() => fetchData());
    }
  };

  const toggleStatus = (template) => {
    if (!template) return;
    api.post('/api/templates/', {
      ...template,
      trigger_id: template.trigger_id, // keep it same
      is_enabled: !template.is_enabled
    }).then(() => fetchData());
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <header>
        <h1>Notification System Admin</h1>
        <button onClick={handleLogout}>Logout</button>
      </header>

      <table className="admin-table">
        <thead>
          <tr>
            <th>Trigger</th>
            <th>WhatsApp</th>
            <th>Email</th>
            <th>Web Push</th>
          </tr>
        </thead>
        <tbody>
          {triggers.map(trigger => (
            <tr key={trigger._id}>
              <td>{trigger.name}</td>
              {['WHATSAPP', 'EMAIL', 'WEB_PUSH'].map(channel => {
                const t = getTemplateForChannel(trigger._id, channel);
                return (
                  <td key={channel}>
                    <div className="cell-content">
                      <span className={`status ${t?.is_enabled ? 'on' : 'off'}`}>
                        {t?.is_enabled ? 'ON' : 'OFF'}
                      </span>
                      <div className="actions">
                        <button onClick={() => handleEdit(trigger._id, channel)}>
                          {t ? 'Edit' : 'Create'}
                        </button>
                        {t && (
                          <button onClick={() => toggleStatus(t)}>
                            Toggle
                          </button>
                        )}
                      </div>
                    </div>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
