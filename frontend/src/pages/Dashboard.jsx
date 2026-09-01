import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import './Dashboard.css';

export default function Dashboard() {
  const [triggers, setTriggers] = useState([]);
  const [templates, setTemplates] = useState({});
  const navigate = useNavigate();

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalData, setModalData] = useState({
    trigger_id: '',
    channel: '',
    title: '',
    subject: '',
    body: '',
    is_enabled: true
  });

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

  const openEditModal = (triggerId, channel) => {
    const template = getTemplateForChannel(triggerId, channel);
    if (template) {
      setModalData(template);
    } else {
      setModalData({
        trigger_id: triggerId,
        channel: channel,
        title: '',
        subject: '',
        body: '',
        is_enabled: true
      });
    }
    setIsModalOpen(true);
  };

  const saveTemplate = async (e) => {
    e.preventDefault();
    try {
      // Ensure nulls are empty strings so Django serializer doesn't fail
      const payload = {
        ...modalData,
        title: modalData.title || '',
        subject: modalData.subject || '',
      };
      await api.post('/api/templates/', payload);
      setIsModalOpen(false);
      fetchData();
    } catch (err) {
      console.error(err.response?.data || err);
      alert("Error saving template: " + JSON.stringify(err.response?.data || {}));
    }
  };

  const toggleStatus = async (template) => {
    if (!template) return;
    try {
      await api.post('/api/templates/', {
        ...template,
        trigger_id: template.trigger_id, 
        is_enabled: !template.is_enabled
      });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div>
          <h1>Notification System Admin</h1>
          <p className="subtitle">Manage all your triggers and channels in one place</p>
        </div>
        <button className="btn-logout" onClick={handleLogout}>Logout</button>
      </header>

      <div className="table-wrapper">
        <table className="premium-table">
          <thead>
            <tr>
              <th>Trigger Event</th>
              <th>WhatsApp</th>
              <th>Email</th>
              <th>Web Push</th>
            </tr>
          </thead>
          <tbody>
            {triggers.map(trigger => (
              <tr key={trigger._id}>
                <td className="trigger-name">
                  <strong>{trigger.name}</strong>
                  <span className="trigger-slug">{trigger.slug}</span>
                </td>
                {['WHATSAPP', 'EMAIL', 'WEB_PUSH'].map(channel => {
                  const t = getTemplateForChannel(trigger._id, channel);
                  return (
                    <td key={channel}>
                      <div className="cell-content">
                        {t ? (
                          <div className="template-status-wrapper">
                            <button 
                              className={`toggle-btn ${t.is_enabled ? 'on' : 'off'}`}
                              onClick={() => toggleStatus(t)}
                              title="Click to toggle status"
                            >
                              {t.is_enabled ? 'Active' : 'Disabled'}
                            </button>
                          </div>
                        ) : (
                          <span className="empty-status">Not Configured</span>
                        )}
                        <button className={`btn-edit ${t ? 'outline' : 'solid'}`} onClick={() => openEditModal(trigger._id, channel)}>
                          {t ? 'Edit' : 'Create'}
                        </button>
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>{modalData._id ? 'Edit Template' : 'Create Template'} - {modalData.channel}</h2>
            <form onSubmit={saveTemplate}>
              <div className="form-group">
                <label>Title (Optional)</label>
                <input 
                  type="text" 
                  value={modalData.title} 
                  onChange={(e) => setModalData({...modalData, title: e.target.value})} 
                  placeholder="Internal Title or Web Push Title"
                />
              </div>
              
              {modalData.channel === 'EMAIL' && (
                <div className="form-group">
                  <label>Subject</label>
                  <input 
                    type="text" 
                    value={modalData.subject || ''} 
                    onChange={(e) => setModalData({...modalData, subject: e.target.value})} 
                    placeholder="Email Subject"
                    required
                  />
                </div>
              )}
              
              <div className="form-group">
                <label>Message Body</label>
                <textarea 
                  value={modalData.body} 
                  onChange={(e) => setModalData({...modalData, body: e.target.value})} 
                  placeholder="Hello {{user_name}}..."
                  required
                  rows={5}
                />
                <small className="help-text">You can use variables like {'{{user_name}}'}</small>
              </div>

              <div className="modal-actions">
                <button type="button" className="btn-cancel" onClick={() => setIsModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn-save">Save Template</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
