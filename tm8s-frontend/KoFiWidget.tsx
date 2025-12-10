import { useEffect } from 'react';

// Declare the Ko-fi widget interface globally so TypeScript recognizes it
declare global {
    interface Window {
        kofiWidgetOverlay: {
            draw: (
                id: string, 
                options: {
                    type: string; 
                    'floating-chat.donateButton.text'?: string;
                    'floating-chat.donateButton.background-color'?: string;
                    'floating-chat.donateButton.text-color'?: string;
                }
            ) => void;
        };
    }
}

const KoFiWidget = () => {
    useEffect(() => {
        // Only proceed if the window object and the widget method are available
        if (typeof window.kofiWidgetOverlay !== 'undefined') {
            window.kofiWidgetOverlay.draw('charmisyoung', {
                'type': 'floating-chat',
                'floating-chat.donateButton.text': 'Tip Me',
                'floating-chat.donateButton.background-color': '#d9534f',
                'floating-chat.donateButton.text-color': '#fff'
            });
        }
        
        // Load the Ko-fi script dynamically only if it hasn't been loaded
        const scriptId = 'kofi-overlay-script';
        if (!document.getElementById(scriptId)) {
            const script = document.createElement('script');
            script.id = scriptId;
            script.src = 'https://storage.ko-fi.com/cdn/scripts/overlay-widget.js';
            document.head.appendChild(script);

            // Important: We need to ensure the `draw` function is called 
            // *after* the script has loaded.
            script.onload = () => {
                 if (typeof window.kofiWidgetOverlay !== 'undefined') {
                    window.kofiWidgetOverlay.draw('charmisyoung', {
                        'type': 'floating-chat',
                        'floating-chat.donateButton.text': 'Tip Me',
                        'floating-chat.donateButton.background-color': '#d9534f',
                        'floating-chat.donateButton.text-color': '#fff'
                    });
                }
            };
        }

    }, []);

    // This component renders nothing itself, it just injects the script/widget
    return null;
};

export default KoFiWidget;