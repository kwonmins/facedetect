from icrawler.builtin import GoogleImageCrawler
import os

# 🔥 저장할 디렉토리 설정
save_dir = "datasets/faces"

# ✅ 폴더 생성 (없으면 자동 생성)
os.makedirs(save_dir, exist_ok=True)

# 🔥 얼굴형별 연예인 크롤링 목록
face_shapes_with_celebrities = {
    "둥근 얼굴 남성": ["강호동", "정형돈", "조정석", "도경수"],
    "각진 얼굴 남성": ["이병헌", "류준열","지성"],
    "계란형 얼굴 남성": ["남주혁", "차은우", "박보검"],
    "긴 얼굴 남성": ["최정훈", "이수혁", "안보현", "김우빈", "김종국"],
    "다이아몬드 얼굴 남성": ["이준기", "류준열", "강동원"],
}

# ✅ 연예인별 50장씩 크롤링 (정제 없이 저장)
for shape, celebs in face_shapes_with_celebrities.items():
    shape_dir = os.path.join(save_dir, shape.replace(" ", "_"))
    os.makedirs(shape_dir, exist_ok=True)

    print(f"🔍 {shape} 크롤링 시작...")

    for celeb in celebs:
        celeb_dir = os.path.join(shape_dir, celeb.replace(" ", "_"))
        os.makedirs(celeb_dir, exist_ok=True)

        google_crawler = GoogleImageCrawler(storage={'root_dir': celeb_dir})

        google_crawler.crawl(
            keyword=f"{celeb} 고해상도 증명사진",
            max_num=150,  # 각 연예인당 50장씩 크롤링
            file_idx_offset=0,
            overwrite=True
        )

print("✅ 모든 크롤링이 완료되었습니다!")
