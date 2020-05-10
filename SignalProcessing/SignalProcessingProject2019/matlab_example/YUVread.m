function YUV = YUVread(fname,dim,frnum)

    % This function reads a frame #frnum (0..n-1) from YUV file into an
    % 3D array with Y, U and V components
    f = fopen(fname,'r');
    
    fseek(f,dim(1)*dim(2)*1.5*frnum,'bof');
    
    % Read Y-component
    Y=fread(f,dim(1)*dim(2),'uchar');
    if length(Y)<dim(1)*dim(2)
        YUV = [];
        return;
    end
    Y=cast(reshape(Y,dim(1),dim(2)),'double')./255;
    
    % Read U-component
    U=fread(f,dim(1)*dim(2)/4,'uchar');
    if length(U)<dim(1)*dim(2)/4
        YUV = [];
        return;
    end
    U=cast(reshape(U,dim(1)/2,dim(2)/2),'double')./255;
    U=imresize(U,2.0);
    
    % Read V-component
    V=fread(f,dim(1)*dim(2)/4,'uchar');
    if length(V)<dim(1)*dim(2)/4
        YUV = [];
        return;
    end    
    V=cast(reshape(V,dim(1)/2,dim(2)/2),'double')./255;
    V=imresize(V,2.0);
    
    % Combine Y, U, and V
    YUV(:,:,1)=Y';
    YUV(:,:,2)=U';
    YUV(:,:,3)=V';
    
    fclose(f);
end