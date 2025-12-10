const KoFiWidget = () => {
  return (
    <div style={{
      position: 'fixed', 
      bottom: '20px',    
      left: '20px',      
      zIndex: 9999,     
    }}>
      <a 
        href='https://ko-fi.com/charmisyoung' 
        target='_blank' 
        rel='noopener noreferrer'
        title="Tip Me"
        style={{ 
          backgroundColor: '#d9534f', 
          color: '#fff',
          textDecoration: 'none',
          padding: '10px 20px', 
          borderRadius: '50px', 
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontFamily: 'sans-serif', 
          fontWeight: '700',
          fontSize: '16px',
          border: 'none',
          cursor: 'pointer',
          boxShadow: '0 4px 12px rgba(0,0,0,0.4)', 
          transition: 'all 0.2s ease',
        }}

        onMouseOver={(e) => {
           e.currentTarget.style.transform = 'scale(1.05)';
           e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.5)';
        }}
        onMouseOut={(e) => {
           e.currentTarget.style.transform = 'scale(1)';
           e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.4)';
        }}
      >
        <img 
          src='https://storage.ko-fi.com/cdn/cup-border.png' 
          alt='Ko-fi cup' 
          style={{ 
            height: '20px', 
            width: 'auto', 
            marginRight: '8px',
            display: 'block' 
          }} 
        />
        Tip Me
      </a>
    </div>
  );
};

export default KoFiWidget;