from typing import Optional, List
from core.domain.agent import AgentSession


class AgentRepository:
    """Repository for managing agent sessions in the system."""
    
    def __init__(self, session=None):
        """Initialize the repository with an optional session.
        
        Args:
            session: Optional database session. If None, uses in-memory
                    storage.
        """
        self._sessions = {}  # In-memory storage
        self.session = session
    
    def save(self, agent_session: AgentSession) -> AgentSession:
        """Save an agent session to the repository.
        
        Args:
            agent_session: The agent session to save
            
        Returns:
            AgentSession: The saved agent session
        """
        if self.session:
            self.session.add(agent_session)
            self.session.commit()
        else:
            self._sessions[agent_session.id] = agent_session
        return agent_session
    
    def get_by_id(self, session_id: str) -> Optional[AgentSession]:
        """Get an agent session by its ID.
        
        Args:
            session_id: The ID of the session to retrieve
            
        Returns:
            Optional[AgentSession]: The session if found, None otherwise
        """
        if self.session:
            return self.session.query(AgentSession).filter_by(id=session_id).first()
        return self._sessions.get(session_id)
    
    def get_all(self) -> List[AgentSession]:
        """Get all agent sessions in the repository.
        
        Returns:
            List[AgentSession]: List of all agent sessions
        """
        if self.session:
            return self.session.query(AgentSession).all()
        return list(self._sessions.values())
    
    def update(self, agent_session: AgentSession) -> AgentSession:
        """Update an existing agent session.
        
        Args:
            agent_session: The agent session to update
            
        Returns:
            AgentSession: The updated agent session
        """
        if self.session:
            self.session.add(agent_session)
            self.session.commit()
        else:
            if agent_session.id not in self._sessions:
                raise ValueError("Agent session not found")
            self._sessions[agent_session.id] = agent_session
        return agent_session
    
    def delete(self, session_id: str) -> bool:
        """Delete an agent session by its ID.
        
        Args:
            session_id: The ID of the session to delete
            
        Returns:
            bool: True if successful
        """
        if self.session:
            session = self.session.query(AgentSession).filter_by(id=session_id).first()
            if not session:
                raise ValueError("Agent session not found")
            self.session.delete(session)
            self.session.commit()
        else:
            if session_id not in self._sessions:
                raise ValueError("Agent session not found")
            del self._sessions[session_id]
        return True 