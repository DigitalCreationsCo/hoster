import FileUpload from '@/components/file-upload';

const UploadPage = () => {
  return (
    <>
      <button onClick={() => window.location.replace("/")} className='close'>x</button>
      <FileUpload />
    </>
  );
};

export default UploadPage;
