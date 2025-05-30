import './App.css';
import {Document, Page} from 'react-pdf';

function App() {
    return(
        <div className="App">
            <Document
            file="../uploadshttps://arxiv.org/pdf/2309.14902.pdf"
            >
                <Page
                    renderAnnotationLayer={false}
                    />
        </Document>
        </div>
    )
}

export default App;