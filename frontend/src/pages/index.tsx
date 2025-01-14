import ProjectList from '@/components/project-list'
import ErrorBoundary from '@/components/error-boundary'

function Home() {
  return (
    <>
    <h1>Welcome to Hoster</h1>
      <h2>Host your project in the cloud in seconds.</h2>
      <a href="/upload"><button>Upload A Project</button></a>
    <ErrorBoundary >
      <ProjectList />
    </ErrorBoundary>
    </>
  )
}

export default Home
