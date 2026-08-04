export interface Resource {
  id: string;
  semester: string;
  course: string;
  category: string;
  rawCategory: string;
  subCategory: string;
  name: string;
  extension: string;
  mimeGroup: string;
  size: number;
  sizeText: string;
  relativePath: string;
  githubUrl: string;
  rawUrl: string;
  previewType: string;
  updatedAt: string;
}

export interface Course {
  semester: string;
  name: string;
  slug: string;
  resourceCount: number;
  categories: Array<{ name: string; count: number }>;
  extensions: Record<string, number>;
  latestUpdatedAt: string;
}

export interface Statistics {
  semesterCount: number;
  courseCount: number;
  resourceCount: number;
  totalSize: number;
  totalSizeText: string;
  semesterResourceCounts: Record<string, number>;
  latestUpdatedAt: string;
  recentResourceIds: string[];
  warningCount: number;
}
