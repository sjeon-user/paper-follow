# 보관 목록 (Keep list)

마음에 든 논문을 **영구 보관**하고 싶으면, 아래에 arXiv id를 **한 줄에 하나씩** 적으세요.
다음 생성(매일 오전 10시 루틴, 또는 수동 실행) 때 코워크가 이 목록을 읽어
`keep.html`(보관함 페이지)에 제목·요약·별점·대표 그림까지 담아 둡니다.
`brief-*.html`이 7일 뒤 삭제돼도 여기 적은 논문은 보관함에 그대로 남습니다.

## 사용법
- `#`으로 시작하는 줄과 빈 줄은 무시됩니다.
- id 뒤에 `· 메모`를 붙이면 보관함에 메모로 함께 표시됩니다(선택).
- 이미 지난(7일 넘어 삭제된) 논문 id를 적어도, 코워크가 arXiv에서 다시 찾아 채웁니다.
- 목록에서 id를 지우면 다음 생성 때 보관함에서도 빠집니다.

## 목록 (여기 아래에 적으세요)
<!-- 예시:
2607.15275 · RoboTTT — 맥락 스케일링이 인상적
2607.18236
-->

Physical Self-Supervised Learning: IMU Sensing without Manual Labels
Yuyang Leng 외 6명 · 2026-07-20 · cs.LG, cs.AI · arXiv:2607.18361
- IMU 부착위치 비정확성 지적.

License: arXiv.org perpetual non-exclusive license
arXiv:2402.10329v3 [cs.RO] 06 Mar 2024
Universal Manipulation Interface: In-The-Wild Robot Teaching Without In-The-Wild Robots
-핸드핼드 그립퍼를 이용한 데이터 collection

License: arXiv.org perpetual non-exclusive license
arXiv:2607.15448v1 [cs.RO] 16 Jul 2026
VTAP Gripper: Synergizing Fingertip Sensing and a Visuo-Tactile Active Palm for Dexterous In-Hand Manipulation
Yuhao Zhou1, Sheeraz Athar1,†, Zhixian Hu1,†,
-메타퀘스트 이용하여 리타게팅

License: CC BY-NC-SA 4.0
arXiv:2607.21071v1 [cs.CV] 23 Jul 2026
TransBiolab: A Real-World Multi-View Dataset of Cluttered Transparent Biomedical Objects
-투명 labware를 대상으로 데이터를 모음. 이의 선행 연구사례 소개 및 비교

arXiv:2303.04137 (cs)
[Submitted on 7 Mar 2023 (v1), last revised 14 Mar 2024 (this version, v5)]
Diffusion Policy: Visuomotor Policy Learning via Action Diffusion
Cheng Chi, Zhenjia Xu, Siyuan Feng, Eric Cousineau, Yilun Du, Benjamin Burchfiel, Russ Tedrake, Shuran Song
-diffusion policy 핸드핼드 논문의 action구현 모델

Ho J, Jain A and Abbeel P (2020) Denoising diffusion probabilistic models.arXiv preprint arXiv:2006.11239 .
-diffusion의 근원

arXiv:2412.03293 (cs)
[Submitted on 4 Dec 2024 (v1), last revised 4 Jun 2025 (this version, v3)]
Diffusion-VLA: Generalizable and Interpretable Robot Foundation Model via Self-Generated Reasoning
-유명한 diffusion VLA

arXiv:2506.09494 (cs)
[Submitted on 11 Jun 2025]
Advances on Affordable Hardware Platforms for Human Demonstration Acquisition in Agricultural Applications
-핸드핼드에 조명을 장착한 사례
-핸드핼드에 조명을 장착한 사례

LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories
	arXiv:2606.13578 [cs.CL]
 	(or arXiv:2606.13578v2 [cs.CL] for this version)
https://doi.org/10.48550/arXiv.2606.13578
Focus to learn more
-실험에 VLA 적용한 사례

Wang, P., Bai, S., Tan, S., Wang, S., Fan, Z., Bai, J., Chen, K., Liu, X., Wang, J., Ge, W., et al.Qwen2-vl: Enhancing vision-language model’s perception of the world at any resolution.arXiv preprint arXiv:2409.12191, 2024
-Qwen2-VL 

TransCut: Transparent Object Segmentation from a Light-Field Image
Published in: 2015 IEEE International Conference on Computer Vision (ICCV)
Date of Conference: 07-13 December 2015
Date Added to IEEE Xplore: 18 February 2016
ISBN Information:
Electronic ISSN: 2380-7504
DOI: 10.1109/ICCV.2015.393
Publisher: IEEE
Conference Location: Santiago, Chile
-투명산 object segmentation 한 사례

투명 물체 × Diffusion

D3RoMa — arXiv:2409.14365 (CoRL 2024)
depth가 아니라 stereo disparity를 diffusion으로 생성하고, 좌우 일관성 제약을 classifier guidance로 걸어 생성 모델의 환각을 기하로 억제합니다.

DKT (Diffusion Knows Transparency) — arXiv:2512.23705 (ICRA 2026)
사전학습된 비디오 diffusion을 그대로 재활용해, 프레임 간 흔들리지 않는 투명체 depth/normal을 뽑습니다. 정책 입력으로 쓸 거라면 이 temporal consistency가 결정적입니다.

TransDiff — arXiv:2503.12779
단일 뷰 RGB-D 한 장에서, segmentation·edge·normal map을 조건으로 걸고 DDPM이 노이즈로부터 depth를 그려냅니다. 멀티뷰 없이 가려는 방향.

Diffusion-Based Depth Inpainting for Transparent and Reflective Objects — arXiv:2410.08567
깨진 depth를 "구멍 난 이미지"로 보고 diffusion inpainting으로 메우는, 가장 직관적인 접근.

TranSplat — arXiv:2502.07840
latent diffusion으로 투명체의 표면 임베딩(SurfEmb)을 생성해 3D Gaussian Splatting과 결합 — depth 대신 명시적 표면 표현을 만듭니다.

ClearDepth — arXiv:2409.08926
스테레오 시뮬레이션의 sim2real을 강화해 투명체 depth를 얻는 라인.

투명 물체 depth completion (diffusion 아님, 비교군으로 필요)

Seeing Glass / TranspareNet — arXiv:2110.00087
point cloud completion과 depth completion을 함께 돌려, 액체가 든 용기까지 포함한 어수선한 장면을 다룹니다. TODD 데이터셋 배출.

TDCNet — arXiv:2412.14961
CNN-Transformer 이중 분기로, 기존 방법들이 버리다시피 한 "망가진 원본 depth" 안의 잔여 정보를 최대한 살려 씁니다.

정책 쪽 — depth 의존을 낮추거나 없애는 방향

Diffusion Policy — arXiv:2303.04137
행동 생성을 조건부 denoising 과정으로 두는 원조 논문. RGB 조건화 + receding horizon control이 핵심 기여이고, 애초에 depth를 필수로 요구하지 않습니다.

DP3 (3D Diffusion Policy) — arXiv:2403.03954
희소 point cloud를 조건으로 쓰는 3D 확장판. 다만 투명체에서는 입력 point cloud 품질이 무너지면서 성능이 급락하는 것이 실험적으로 확인된 쪽입니다.

VO-DP — arXiv:2510.15530
depth 센서 없이, VGGT의 기하 특징과 DINOv2의 의미 특징을 cross-attention으로 융합해 단일 뷰 RGB만으로 diffusion policy를 돌립니다.

VolumeDP — arXiv:2603.17720
RGB-only인데 2D 특징을 volumetric 표현으로 lift한 뒤 spatial token으로 압축 — depth 센서 없이 공간 추론을 회복하려는 시도.

SCDP (Spatially Conditioned Diffusion Policy) — arXiv:2606.14535
end-effector 궤적 자체를 시각적 attention anchor로 삼아, 단일 RGB 카메라만으로 정밀 조작을 달성합니다.
