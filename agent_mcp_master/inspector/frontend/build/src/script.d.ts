declare global {
    interface Window {
        hljs: {
            highlightElement: (element: HTMLElement) => void;
        };
    }
}
export {};
