import React from 'react'

export default class ErrorBoundary extends React.Component<{
  fallback?: React.ReactNode;
  children: React.ReactNode;
}, 
{ hasError: boolean; error: string; }> {
    constructor(props: any) {
      super(props);
      this.state = { hasError: false, error: '' };
    }
  
    static getDerivedStateFromError(error: Error) {
      // Update state so the next render will show the fallback UI.
      return { hasError: true, error: error.message };
    }
  
    componentDidCatch(error: Error, errorInfo: any) {
      // You can also log the error to an error reporting service
      // logErrorToMyService(error, errorInfo);
      console.error('did catch error')
      console.error(error)
      console.error(errorInfo)
    }
  
    render() {
      if (this.state.hasError) {
        // You can render any custom fallback UI
        return this.props.fallback || <h2 style={{color: 'red'}}>{this.state.error || 'Something went wrong.'}</h2>;
      }
  
      return this.props.children; 
    }
  }