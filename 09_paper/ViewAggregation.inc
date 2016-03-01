% ---------------------------------------------------------------------
% EG author guidelines plus sample file for EG publication using LaTeX2e input
% D.Fellner, v1.17, Sep 23, 2010


\title{\vspace{-1cm}3D Model Signatures via Aggregation of Multi-view CNN Features\vspace{-1cm}}

\author{Yangyan Li$^{1,2}$, Noa Fish$^{1}$, Daniel Cohen-Or$^{1}$ and Baoquan Chen$^{2}$\vspace{-0.3cm}
        \\
         $^1$Tel Aviv University, Israel \qquad $^2$Shandong University, China\vspace{-2cm}
       }

%-------------------------------------------------------------------------
\begin{document}


\teaser{
\vspace{-0.5cm}
 \includegraphics[width=\linewidth]{cnn_architectures}
 \centering
  \caption{CNN architectures for extracting 3D model signatures by aggregating CNN features of the multi-view images rendered from the 3D models. Mutli-view CNN features are aggregated by concatenating the CNN extracted view features when consistent 3D model orientation is avaiable (left), or max-pooling them when the model orientations are unknown (right).}
\label{fig:cnn_architectures}
}

\maketitle

%\begin{abstract}
%\end{abstract}

%-------------------------------------------------------------------------
\section{Method Description}

3D models can be rendered into multiple view images, thus their signatures can be represented by the multi-view image features~\cite{chen2003visual}. In this way, the informativeness and discriminativeness of the image features play critical role in the quality of the 3D model signatures. In recent few years, CNN extracted image features have been shown to be very successful in image based recognition tasks, as they are both informative and discriminative. Such advances in image feature extraction can be levereged to boost the performance of 3D model signatures.

Following~\cite{su2015multi}, we represent 3D model signatures with CNN features from multi-view images rendered from the 3D models. We first extract CNN features for each rendered view with the convolutional layers of a CNN model fine tuned for classifying individual rendered view into the category and sub-category of the 3D models, then aggregate the view features, and finally train several fully connected layers on classification tasks based on the aggregated features.

The key of this approach is the aggregation of CNN features from different views. In~\cite{su2015multi}, the view features are aggregated by a max-pooling, which treats different views evenly, thus is independent of how the rendering views are chosen. This is an advantage when the model orientations are unknown, but a disadvantage when the models are already consistently aligned. An aggregation method that is aware of the consistency should perform better on consistently aligned models. Instead of using max-pooling, we aggregate multi-view CNN features by concatenating the view features for 3D models with consistent orientations. In the concatenation based view feature aggregation, the fully connected layers can leverage the consistency of the rendered views, and make decisions based on an holistic understanding of all views. See Figure~\ref{fig:cnn_architectures} for these CNN architectures.

More specifically, we render each model from 12 evenly distributed views, and fine tune VGG-19 network~\cite{simonyan2014very} for the convolutional layers that is used for view feature extraction. We open source our code at \url{http://yangyanli.github.io/SHREC2016/} for reproducing our results.

%-------------------------------------------------------------------------
%\bibliographystyle{eg-alpha}
\bibliographystyle{eg-alpha-doi}

\bibliography{ViewAggregation}
%-------------------------------------------------------------------------

\end{document}
