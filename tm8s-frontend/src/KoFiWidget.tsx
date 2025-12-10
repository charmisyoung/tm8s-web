import React from 'react';

const KoFiWidget = () => {
  return (
    <a 
      href='https://ko-fi.com/charmisyoung' 
      target='_blank' 
      rel='noopener noreferrer'
      title="Support me on Ko-fi"
      style={{ 
        backgroundColor: '#d9534f', 
        color: '#fff',
        textDecoration: 'none',
        padding: '6px 12px', 
        borderRadius: '20px',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'sans-serif',
        fontWeight: '600',
        fontSize: '12px',
        border: 'none',
        cursor: 'pointer',
        boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        transition: 'transform 0.2s ease',
      }}
      onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
      onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
    >
      <img 
        src='https://storage.ko-fi.com/cdn/cup-border.png' 
        alt='Ko-fi' 
        style={{ 
          height: '14px', 
          width: 'auto', 
          marginRight: '6px' 
        }} 
      />
      Tip Me
    </a>
  );
};

export default KoFiWidget;