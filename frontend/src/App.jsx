import ChatWindow from "./components/ChatWindow";
import HistoryContainer from "./components/HistoryContainer.jsx";
import './App.css'

function App() {
  return (
      <div className="app-container">
          <div className="chat-container-index">
              <ChatWindow />
          </div>
          <div className="chat-history-container-index">
              <HistoryContainer />
          </div>
      </div>
  );
}

export default App;
