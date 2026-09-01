import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import './Dashboard.css';

export default function Dashboard() {
  const [triggers, setTriggers] = useState([]);
  const [templates, setTemplates] = useState({});
  const navigate = useNavigate();

  // Edit Template Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalData, setModalData] = useState({
    trigger_id: '',
    channel: '',
    title: '',
    subject: '',
    body: '',
    is_enabled: true
  });

  // Add Trigger Modal State
  const [isTriggerModalOpen, setIsTriggerModalOpen] = useState(false);
  const [triggerName, setTriggerName] = useState('');

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
        title: template.title || '',
        subject: template.subject || '',
        trigger_id: template.trigger_id, 
        is_enabled: !template.is_enabled
      });
      fetchData();
    } catch (err) {
      console.error(err);
      alert("Error toggling: " + JSON.stringify(err.response?.data || {}));
    }
  };

  const saveTrigger = async (e) => {
    e.preventDefault();
    if (!triggerName) return;
    
    // Auto generate a slug from the name (e.g. "Password Reset" -> "password_reset")
    const slug = triggerName.toLowerCase().replace(/ /g, '_').replace(/[^\w-]+/g, '');
    
    try {
      await api.post('/api/triggers/', {
        name: triggerName,
        slug: slug,
        event_type: "CUSTOM_EVENT"
      });
      setTriggerName('');
      setIsTriggerModalOpen(false);
      fetchData();
    } catch (err) {
      alert("Error creating trigger: " + JSON.stringify(err.response?.data || {}));
    }
  };

  const handleTestSend = async (triggerSlug) => {
    try {
      // Get the logged in user from localStorage
      const userStr = localStorage.getItem('user');
      const user = userStr ? JSON.parse(userStr) : null;
      if (!user) {
        alert("Could not identify current user.");
        return;
      }
      
      alert(`Sending test notification for '${triggerSlug}'...`);
      await api.post('/api/notifications/trigger/', {
        trigger_slug: triggerSlug,
        user_id: user.id || user._id,
        variables: {
          user_name: user.name || "Test User",
          amount: "$99.99",
          order_id: "ORD-12345",
          login_time: new Date().toLocaleTimeString(),
          logout_time: new Date().toLocaleTimeString(),
          reset_link: "https://yourwebsite.com/reset-password"
        }
      });
      alert("✅ Test Send Successful! Check your email/phone/browser.");
    } catch (err) {
      alert("❌ Error sending test: " + JSON.stringify(err.response?.data || err.message));
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
        <div className="header-actions">
          <button className="btn-add-trigger" onClick={() => setIsTriggerModalOpen(true)}>+ Add Trigger</button>
          <button className="btn-logout" onClick={handleLogout}>Logout</button>
        </div>
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
                            <div 
                              className={`toggle-switch ${t.is_enabled ? 'on' : 'off'}`}
                              onClick={() => toggleStatus(t)}
                              title="Click to toggle status"
                            >
                              <div className="toggle-slider"></div>
                              <span className="toggle-label">{t.is_enabled ? 'ON' : 'OFF'}</span>
                            </div>
                          </div>
                        ) : (
                          <span className="empty-status">Not Configured</span>
                        )}
                        <div className="btn-group">
                          <button className={`btn-edit ${t ? 'outline' : 'solid'}`} onClick={() => openEditModal(trigger._id, channel)}>
                            {t ? 'Edit' : 'Create'}
                          </button>
                          {t && (
                            <button className="btn-test" onClick={() => handleTestSend(trigger.slug)} title="Send a test notification">
                              Test
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

      {isTriggerModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content" style={{maxWidth: '400px'}}>
            <h2>Create New Trigger</h2>
            <form onSubmit={saveTrigger}>
              <div className="form-group">
                <label>Trigger Name</label>
                <input 
                  type="text" 
                  value={triggerName} 
                  onChange={(e) => setTriggerName(e.target.value)} 
                  placeholder="e.g. Password Reset"
                  required
                />
                <small className="help-text">A unique slug will be automatically generated.</small>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-cancel" onClick={() => setIsTriggerModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn-save">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
