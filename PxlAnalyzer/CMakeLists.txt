add_library(PxlAnalyzer
    EventClassFactory/ParticleMap.cpp
    EventClassFactory/TriggerStream.cpp
    EventClassFactory/EventClassFactory.cpp
    EventClassFactory/Resolutions.cpp
    Pxl/Pxl/src/Vertex.cpp
    Pxl/Pxl/src/ObjectManager.cpp
    Pxl/Pxl/src/Object.cpp
    Pxl/Pxl/src/Event.cpp
    Pxl/Pxl/src/ConfigLoader.cpp
    Pxl/Pxl/src/InputHandler.cpp
    Pxl/Pxl/src/Variant.cpp
    Pxl/Pxl/src/AnalysisProcess.cpp
    Pxl/Pxl/src/WkPtrBase.cpp
    Pxl/Pxl/src/FileFactory.cpp
    Pxl/Pxl/src/Relative.cpp
    Pxl/Pxl/src/InformationChunk.cpp
    Pxl/Pxl/src/Random.cpp
    Pxl/Pxl/src/ChunkWriter.cpp
    Pxl/Pxl/src/ObjectFactory.cpp
    Pxl/Pxl/src/StdFileImpl.cpp
    Pxl/Pxl/src/LocalFileImpl.cpp
    Pxl/Pxl/src/PluginManager.cpp
    Pxl/Pxl/src/OutputHandler.cpp
    Pxl/Pxl/src/Hep.cpp
    Pxl/Pxl/src/NamedTMPFile.cpp
    Pxl/Pxl/src/Configuration.cpp
    Pxl/Pxl/src/BasicContainer.cpp
    Pxl/Pxl/src/EventView.cpp
    Pxl/Pxl/src/ObjectOwner.cpp
    Pxl/Pxl/src/SoftRelations.cpp
    Pxl/Pxl/src/functions.cpp
    Pxl/Pxl/src/Collision.cpp
    Pxl/Pxl/src/OutputFile.cpp
    Pxl/Pxl/src/BasicNVector.cpp
    Pxl/Pxl/src/File.cpp
    Pxl/Pxl/src/BasicMatrix.cpp
    Pxl/Pxl/src/Core.cpp
    Pxl/Pxl/src/LorentzVector.cpp
    Pxl/Pxl/src/Tokenizer.cpp
    Pxl/Pxl/src/dCapFileImpl.cpp
    Pxl/Pxl/src/ChunkReader.cpp
    Pxl/Pxl/src/Particle.cpp
    Pxl/Pxl/src/MessageDispatcher.cpp
    Pxl/Pxl/src/AnalysisFork.cpp
    Pxl/Pxl/src/Relations.cpp
    Pxl/Pxl/src/sFTPFileImpl.cpp
    Pxl/Pxl/src/Id.cpp
    Pxl/Pxl/src/Basic3Vector.cpp
    Pxl/Pxl/src/UserRecord.cpp
    Pxl/Pxl/src/logging.cpp
    Main/JetResolution.cpp
    Main/EventAdaptor.cpp
    #Main/NanoAODReader.cpp
    Main/SkipEvents.cpp
    Main/GammaSelector.cpp
    Main/PDFTool.cpp
    Main/RunLumiRanges.cpp
    Main/BinnedMapping.cpp
    Main/MuonSelector.cpp
    Main/METSelector.cpp
    Main/JetTypeWriter.cpp
    Main/OldNameMapper.cpp
    Main/ReWeighter.cpp
    Main/ScaleFactor.cpp
    Main/JetSelector.cpp
    Main/ParticleSplittingFunctions.cpp
    Main/EleSelector.cpp
    Main/EventCleaning.cpp
    Main/TriggerGroup.cpp
    Main/TriggerSelector.cpp
    Main/EventSelector.cpp
    Main/EffectiveArea.cpp
    Main/ParticleMatcher.cpp
    Main/PhotonEffectiveArea.cpp
    Main/TauSelector.cpp
    Main/Systematics.cpp
    Main/GenSelector.cpp
    Main/FatJetSelector.cpp
    Main/ObjectSelector.cpp
    Main/SystematicsInfo.cpp
    Tools/dCache/dCacheBuf.cpp
    Tools/MConfig.cpp
    Tools/SignalHandler.cpp
    Tools/AnyOption.cpp
    Tools/Tools.cpp
    Main/TOMLConfig.cpp
)
target_include_directories(PxlAnalyzer PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_options(PxlAnalyzer PUBLIC -g -c -Wno-narrowing)
