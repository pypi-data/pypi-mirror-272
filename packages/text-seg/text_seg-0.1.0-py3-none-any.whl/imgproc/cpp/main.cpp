#include "Binarization.hpp"
#include "Scanner.hpp"
#include "LineSegmentation.hpp"
#include <filesystem>
#include <string>

namespace fs = std::filesystem;

int main(int argc, char *argv[]) {

    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <input_image_path> <output_directory_path>\n";
        return 1;
    }

    std::string srcPath = argv[1];
    std::string outPath = argv[2];

    cv::Mat image = cv::imread(srcPath);

    if (image.empty()) {
        std::cerr << "Error: Could not open or read the image file\n";
        return 1;
    }

    std::string name = fs::path(outPath).filename().replace_extension("").string();
    std::string extension = ".png";

    fs::create_directories(outPath);

    // START Step 1: crop //
    Scanner scanner;
    cv::Mat imageCropped;
    scanner.process(image, imageCropped);

    // START Step 1.1: resize and definitions //
    int newW = 1280;
    int newH = ((newW * imageCropped.rows) / imageCropped.cols);
    cv::resize(imageCropped, imageCropped, cv::Size(newW, newH));

    int chunksNumber = 8;
    int chunksProcess = 4;
    // END Step 1.1 //

    // START Step 2: binarization //
    Binarization threshold;
    cv::Mat imageBinary;
    // default = 0 | otsu = 1 | niblack = 2 | sauvola = 3 | wolf = 4 //
    threshold.binarize(imageCropped, imageBinary, true, 3);

    // START Step 3: line segmentation //
    LineSegmentation line;
    std::vector<cv::Mat> lines;
    cv::Mat imageLines = imageBinary.clone();
    line.segment(imageLines, lines, chunksNumber, chunksProcess);
    
    // Save segmented lines directly in outPath
    for (size_t i = 0; i < lines.size(); ++i) {
        std::string lineName = std::to_string(i) + extension;
        fs::path saveLine = fs::path(outPath) / lineName; // Construct full path directly in outPath
        cv::imwrite(saveLine.u8string(), lines[i]);
    }

    

    // Save segmented lines
    //for (size_t i = 0; i < lines.size(); ++i) {
    //    std::string lineName = std::to_string(i) + extension;
        //std::string lineName = name + "_line_" + std::to_string(i) + extension;
       // fs::path saveLine = fs::path(outPath) / lineName;
       // cv::imwrite(saveLine.u8string(), lines[i]);
   // }

    return 0;
}

